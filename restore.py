from sympy.physics.control.control_plots import plt
import copy
import numpy as np
import parsers


def gram_schmidt(vectors):
    """Ортогонализируем набор векторов с помощью процесса Грама-Шмидта"""
    orthogonal_vectors = []
    for v in vectors:
        w = v - sum(np.dot(v, u) / np.dot(u, u) * u for u in orthogonal_vectors)
        orthogonal_vectors.append(w)
    return np.array(orthogonal_vectors)


def project_onto_basis(v, basis):
    """Проецируем вектор на базис"""
    return np.array([np.dot(v, b) / np.dot(b, b) for b in basis])


def decompose_vector(v, non_orthogonal_basis):
    """Разлагаем вектор по неортогональному базису"""
    # Ортогонализируем базис
    orthogonal_basis = gram_schmidt(non_orthogonal_basis)

    # Находим коэффициенты в ортогональном базисе
    coeffs_orthogonal = project_onto_basis(v, orthogonal_basis)

    # Решаем систему линейных уравнений для нахождения исходных коэффициентов
    try:
        coeffs_original = np.linalg.solve(orthogonal_basis.T, coeffs_orthogonal)
    except Exception:
        return [0 for i in range(len(orthogonal_basis))]

    return coeffs_original

def normalized_similarity_percentage(set1, set2):
    # Проверка, что оба набора имеют одинаковую длину
    if len(set1) != len(set2):
        raise ValueError("Наборы должны иметь одинаковую длину.")

    # Преобразование списков в numpy массивы
    set1 = np.array(set1)
    set2 = np.array(set2)

    # Вычисление евклидова расстояния
    distance = np.linalg.norm(set1 - set2)

    # Нормализация расстояния
    max_distance = np.linalg.norm(set1) + np.linalg.norm(set2)

    if max_distance == 0:
        # Если оба набора состоят только из нулей, считаем их полностью схожими (100%)
        return 100.0

    # Нормализованное сходство
    similarity = 1 - distance / max_distance

    # Переводим в проценты
    return similarity * 100


def accuracy_metric(v1, v2):
    return normalized_similarity_percentage(v1, v2)


def approximate_with_non_orthogonal_basis(vector, basis):
    vector = copy.deepcopy(vector)
    basis = copy.deepcopy(basis)
    A = np.column_stack(basis)
    coefficients, residuals, _, _ = np.linalg.lstsq(A, vector, rcond=None)
    approximation = np.dot(A, coefficients)
    return approximation, coefficients

def approximate_with_non_orthogonal_basis_orto(vector, basis):
    vector_copy = copy.deepcopy(vector)
    basis_copy = copy.deepcopy(basis)
    coofs = decompose_vector(vector_copy,basis_copy)
    aprox = [coofs[i]*basis[i] for i in range(len(basis))]
    return aprox, coofs

def coof_evolution(mariogram, fk, mariogram_answer):
    # recovery_data = []
    res = []
    for t in range(len(mariogram)):
        aprox, coof = approximate_with_non_orthogonal_basis_orto(mariogram[:t + 1], [fki[:t + 1] for fki in fk])
        accuracy = sum(abs(mariogram[:t + 1] - aprox))
        res.append([accuracy, coof])
    # fig, ax1 = plt.subplots(1)
    # acc = [res[i][0] for i in range(len(res))]
    coofs = [[*res[i][1]] for i in range(len(res))]
    acc = [accuracy_metric(np.array(mariogram_answer), coofs[t]) for t in range(len(mariogram))]
    return acc, mariogram, coofs


def coof_evolution_plot(mariogram, fk, mariogram_answer):
    acc, mariogram, coofs = coof_evolution(mariogram, fk, mariogram_answer)
    fig, [ax1, ax2, ax3] = plt.subplots(3)
    ax1.plot(mariogram)
    ax2.plot(acc)
    transposed_data = list(zip(*coofs))
    transposed_data = [list(item) for item in transposed_data]
    [ax3.plot(np.clip(transposed_data[i], -10, max(*coofs[-1]))) for i in range(len(transposed_data))]
    plt.show()


def evolution(wave_form_to_restore: parsers.WaveFormToRestore, pos):
    return coof_evolution_plot(wave_form_to_restore.mariorgams[pos], [fki[pos] for fki in wave_form_to_restore.fk],
                               wave_form_to_restore.answers)


def find_stable_index(accuracy_list, threshold):
    for i in range(len(accuracy_list)):
        # Проверяем, что все элементы после i-го, включая его самого, не опускаются ниже threshold
        if all(accuracy >= threshold for accuracy in accuracy_list[i:]):
            return i
    return -1  # Если такого элемента нет


def get_restore_time(wave_form_to_restore: parsers.WaveFormToRestore, pos, threshold):
    acc, mariogram, coofs = coof_evolution(wave_form_to_restore.mariorgams[pos],
                                           [fki[pos] for fki in wave_form_to_restore.fk],
                                           wave_form_to_restore.answers)
    return find_stable_index(acc, threshold)


if __name__ == "__main__":
    evolution(parsers.WaveFormToRestore("octo", "1_2_4_8_16_32"), "700_1100")
    # wave_form_to_restore = parsers.WaveFormToRestore("quadro", "8_4_0_-4")
    # pos = "700_800"
    # print(get_restore_time(wave_form_to_restore, pos, 95))
