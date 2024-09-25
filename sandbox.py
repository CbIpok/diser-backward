import numpy as np


# Функция для ортогонализации системы векторов по методу Грама-Шмидта
def gram_schmidt(vectors):
    orthogonal_vectors = []
    for i in range(len(vectors)):
        # Проекция текущего вектора на уже ортогонализированные векторы
        new_vector = vectors[i]
        if i == 0:
            orthogonal_vectors.append(new_vector)
        else:
            for j in range(i):
                proj = np.dot(new_vector, orthogonal_vectors[j]) / np.dot(orthogonal_vectors[j],
                                                                          orthogonal_vectors[j]) * orthogonal_vectors[j]
                new_vector = new_vector - proj
            orthogonal_vectors.append(new_vector)
    return np.array(orthogonal_vectors)


# Функция для разложения вектора по ортогональному базису
def decompose_vector(v, orthogonal_basis):
    coefficients = []
    for u in orthogonal_basis:
        # Обработка возможного деления на ноль (в случае линейной зависимости)
        try:
            coefficient = np.dot(v, u) / np.dot(u, u)
        except ZeroDivisionError:
            coefficient = 0
        coefficients.append(coefficient)
    return np.array(coefficients)


# Вычисление l_k_i для конкретных индексов k и i
def compute_l_k_i(f_k_i, e_i):
    dot_product_fk_ei = np.dot(f_k_i, e_i)
    dot_product_ei_ei = np.dot(e_i, e_i)

    # Проверка на деление на ноль
    if dot_product_ei_ei == 0:
        return 0
    else:
        return -dot_product_fk_ei / dot_product_ei_ei


# Функция для вычисления F(j, i)
def F(j, i, l):
    if j == i:
        return 0
    elif j == i + 1:
        return l[j, i]
    else:
        sum_part = sum(l[j, k] * F(k, i, l) for k in range(i + 1, j))
        return l[j, i] + sum_part


# Вычисление bi
def compute_bi(k, a_k, l):
    b = np.zeros_like(a_k)

    # По формулам из задачи
    b[k] = a_k[k]
    b[k - 1] = a_k[k - 1] + a_k[k] * F(k, k - 1, l)
    b[k - 2] = a_k[k - 2] + a_k[k - 1] * F(k - 1, k - 2, l) + a_k[k] * F(k, k - 2, l)

    for i in range(k - 3, -1, -1):
        sum_part = sum(a_k[j] * F(j, i, l) for j in range(i + 1, k + 1))
        b[i] = a_k[i] + sum_part

    return b


# Основная функция для аппроксимации вектора x в базисе fk
def approximate_vector(x, f_k):
    try:
        # Ортогонализация базиса
        e_i = gram_schmidt(f_k)

        # Разложение вектора x по ортогональному базису
        a_k = decompose_vector(x, e_i)

        # Вычисление l_k_i
        l_k_i = np.zeros((len(f_k), len(e_i)))
        for k in range(len(f_k)):
            for i in range(len(e_i)):
                l_k_i[k, i] = compute_l_k_i(f_k[k], e_i[i])

        # Вычисление b_i
        k = len(a_k) - 1
        b = compute_bi(k, a_k, l_k_i)
        return b

    except Exception as e:
        # В случае исключения (например, линейной зависимости) возвращаем нулевые коэффициенты
        print("Ошибка при аппроксимации, возвращены нулевые коэффициенты:", e)
        return np.zeros(len(x))


# Пример использования
x = [1, 2, 3, 4]
f_k = np.array([[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]])  # базис fk

# Выводим аппроксимированные коэффициенты bi
b = approximate_vector(x, f_k)
print("Коэффициенты bi:", b)
print("Сумма аппроксимированных векторов:", sum([b[i] * f_k[i] for i in range(len(b))]))
