import json

import yappi
from sympy.physics.control.control_plots import plt
import copy
import numpy as np
from tqdm import tqdm

import parsers
import restore_save
# from sandbox2 import Wave, Basis
import sys
sys.path.append(r'D:\dmitrienkomy\cpp\diser\out\build\x64-Release')
# import approx_orto
import apporox

def gram_schmidt_with_fixed_first_vector(vectors):
    """Ортогонализация системы векторов методом Грама-Шмидта, фиксируя первый вектор."""
    orthogonal_basis = [vectors[0].astype(float)]  # Первый вектор остаётся неизменным
    for v in vectors[1:]:
        v = v.astype(float)
        for u in orthogonal_basis:
            # Оптимизированная операция вычитания с использованием NumPy
            v -= np.dot(v, u) / np.dot(u, u) * u
        orthogonal_basis.append(v)
    return orthogonal_basis


def decompose_vector(vector, basis):
    """Находит коэффициенты разложения вектора по базису."""
    # Используем векторизацию с NumPy для вычисления коэффициентов
    basis_norms = np.array([np.dot(b, b) for b in basis])
    coefficients = np.dot(vector, np.array(basis).T) / basis_norms
    return coefficients


def find_coefficients_in_original_basis(basis, orthogonal_basis, f_bort):
    """Находит коэффициенты разложения вектора по исходному базису из ортогонализованного."""
    # Создание матрицы перехода с использованием NumPy
    transition_matrix = np.dot(basis, np.array(orthogonal_basis).T)

    # Решение системы уравнений
    norm_factors = np.array([np.dot(ob, ob) for ob in orthogonal_basis])
    f_b = np.linalg.solve(transition_matrix.T, f_bort * norm_factors)

    return f_b


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

def approximate_with_non_orthogonal_basis_orto_cpp(vector, basis):
    return None, apporox.approximate_vector(vector,basis)

def approximate_with_non_orthogonal_basis_orto(vector, basis):
    # Убираем глубокое копирование
    bort = gram_schmidt_with_fixed_first_vector(basis)
    f_bort = decompose_vector(vector, bort)

    try:
        # Оптимизируем нахождение коэффициентов
        coofs = find_coefficients_in_original_basis(basis, bort, f_bort)
    except np.linalg.LinAlgError:
        return None, None

    # Оптимизированное вычисление аппроксимации
    aprox = np.dot(coofs, np.array(basis))

    return aprox, coofs

def coof_evolution(mariogram, fk, mariogram_answer,approximate):
    # recovery_data = []
    res = []
    for t in tqdm(range(len(mariogram))):
        aprox, coof = approximate(mariogram[:t + 1], [fki[:t + 1] for fki in fk])
        if aprox is None or coof is None:
            accuracy = 1000000000
            coof = [0 for i in range(len(fk))]
        else:
            accuracy = sum(abs(mariogram[:t + 1] - aprox))
        res.append([accuracy, coof])
    # fig, ax1 = plt.subplots(1)
    # acc = [res[i][0] for i in range(len(res))]
    coofs = [[*res[i][1]] for i in range(len(res))]
    acc = [accuracy_metric(np.array(mariogram_answer), coofs[t]) for t in range(len(mariogram))]
    return acc, mariogram, coofs

def coof_evolution_save(mariogram, fk, mariogram_answer):
    acc, mariogram, coofs = coof_evolution(mariogram, fk, mariogram_answer, approximate_with_non_orthogonal_basis_orto)
    # coofs = approx_orto.approximate_with_non_orthogonal_basis_orto_t(mariogram,fk)
    # acc_lsqr, mariogram_lsqr, coofs_lsqr = coof_evolution(mariogram, fk, mariogram_answer,
    #                                                       approximate_with_non_orthogonal_basis)
    obj_orto = {"mariorgam" : mariogram,"coofs":coofs,"fk":fk}
    # obj_lsqr = {"mariorgam" : mariogram,"coofs":coofs_lsqr,"fk":fk}
    return obj_orto



def coof_evolution_plot(mariogram, fk, mariogram_answer):
    acc, mariogram, coofs = coof_evolution(mariogram, fk, mariogram_answer,approximate_with_non_orthogonal_basis)
    f = coofs[-1]
    # Вектор, с которым будем сравнивать
    # acc_lsqr, mariogram_lsqr, coofs_lsqr = coof_evolution(mariogram, fk, mariogram_answer, approximate_with_non_orthogonal_basis)
    fig, [ax1, ax2, ax3,ax5,ax4] = plt.subplots(5)
    ax1.plot(mariogram)
    ax2.plot(acc)
    ax2.scatter(find_stable_index(acc, restore_save.threshold), 0)
    transposed_data = list(zip(*coofs))
    transposed_data = [list(item) for item in transposed_data]
    [ax3.plot(np.clip(transposed_data[i], -10, max(*coofs[-1]))) for i in range(len(transposed_data))]
    [ax3.scatter(len(mariogram),mariogram_answer[i]) for i in range(len(mariogram_answer))]
    [ax4.plot(fk[i]) for i in range(len(fk))]
    # transposed_data = list(zip(*coofs_lsqr))
    transposed_data = [list(item) for item in transposed_data]
    [ax5.plot(np.clip(transposed_data[i], -10, max(*coofs[-1]))) for i in range(len(transposed_data))]
    [ax5.scatter(len(mariogram), mariogram_answer[i]) for i in range(len(mariogram_answer))]
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
                                           wave_form_to_restore.answers,approximate_with_non_orthogonal_basis_orto)
    return find_stable_index(acc, threshold)

def numpy_to_python(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Преобразуем массив numpy в список
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)  # Преобразуем numpy-числа в int
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)  # Преобразуем numpy-числа в float
    else:
        raise TypeError(f"Type {type(obj)} not serializable")

if __name__ == "__main__":
    # evolution(parsers.WaveFormToRestore("octo", "1_2_4_8_16_32"), "700_1100")

    db_path = 'c:/vm_share/set_1.db'  # Замените на ваш путь к базе данных
    bath_name = '/mnt/hgfs/shared/set_1/bathes/2048_100_1000.bath'
    basis_pattern = 'square_center_basis_144'
    wave = Wave(bath_name, 0, db_path).get_mariogram(f"{0}_{0}")
    basis = Basis(bath_name,basis_pattern,db_path).get_mariogram(f"{0}_{0}")
    obj = {"mariogramm": wave,"fk": basis}
    with open("data.json", "w") as f:
        json.dump(obj, f, default=numpy_to_python, indent=4)
    # yappi.start()  # Начало профилирования
    coof_evolution(wave,basis, [0]*len(basis))
    # yappi.stop()  # Остановка профилирования
    # # Вывод отчета
    # yappi.get_func_stats().print_all()
    # res = {}
    # for x in range(0,44,15):
    #     for y in range(0, 118, 40):
    #         wave = Wave(bath_name,0,db_path).get_mariogram(f"{x}_{y}")
    #         basis = Basis(bath_name,basis_pattern,db_path).get_mariogram(f"{x}_{y}")
    #         res[f"{x}_{y}"] = coof_evolution_save(wave,basis,
    #                             [0]*len(basis))
    #     with open('output.json', 'w') as json_file:
    #         json.dump(res, json_file, indent=4)
    # wave_form_to_restore = parsers.WaveFormToRestore("quadro", "8_4_0_-4")
    # pos = "700_800"
    # print(get_restore_time(wave_form_to_restore, pos, 95))
