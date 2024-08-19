from sympy.physics.control.control_plots import plt
import copy
import numpy as np
import parsers


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


def coof_evolution(mariogram, fk, mariogram_answer):
    # recovery_data = []
    res = []
    for t in range(len(mariogram)):
        aprox, coof = approximate_with_non_orthogonal_basis(mariogram[:t + 1], [fki[:t + 1] for fki in fk])
        accuracy = sum(abs(mariogram[:t + 1] - aprox))
        res.append([accuracy, coof])
    # fig, ax1 = plt.subplots(1)
    # acc = [res[i][0] for i in range(len(res))]
    coofs = [[*res[i][1]] for i in range(len(res))]
    acc = [accuracy_metric(np.array(mariogram_answer), coofs[t]) for t in range(len(mariogram))]
    return acc, mariogram, coofs


def coof_evolution_plot(mariogram, fk, mariogram_answer):
    acc, mariogram, coofs = coof_evolution(mariogram, fk, mariogram_answer)
    fig, [ax1, ax2] = plt.subplots(2)
    ax1.plot(mariogram)
    ax2.plot(acc)
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



# # evolution(parsers.WaveFormToRestore("quadro", "8_4_0_-4"), "700_800")
# wave_form_to_restore = parsers.WaveFormToRestore("quadro", "8_4_0_-4")
# pos = "700_800"
# print(get_restore_time(wave_form_to_restore, pos, 95))