import numpy as np
import parsers


def gram_schmidt_with_fixed_first_vector(vectors):
    """Ортогонализация системы векторов методом Грама-Шмидта, фиксируя первый вектор."""
    orthogonal_basis = [vectors[0].astype(float)]  # Первый вектор остаётся неизменным
    for v in vectors[1:]:
        v = v.astype(float)
        for u in orthogonal_basis:
            v -= np.dot(v, u) / np.dot(u, u) * u
        orthogonal_basis.append(v)
    return orthogonal_basis


def decompose_vector(vector, basis):
    """Находит коэффициенты разложения вектора по базису."""
    coefficients = []
    for b in basis:
        coefficient = np.dot(vector, b) / np.dot(b, b)
        coefficients.append(coefficient)
    return np.array(coefficients)


def find_coefficients_in_original_basis(basis, orthogonal_basis, f_bort):
    """Находит коэффициенты разложения вектора по исходному базису из ортогонализованного."""
    # Решаем систему f_b * b = f_bort * bort
    transition_matrix = np.array([[np.dot(ob, b) for ob in orthogonal_basis] for b in basis])
    f_b = np.linalg.solve(transition_matrix.T, f_bort * np.array([np.dot(ob, ob) for ob in orthogonal_basis]))
    return f_b


wave_form_to_restore = parsers.WaveFormToRestore("quadro", "8_4_0_-4")

# Пример данных
# b = [np.array([1, 1, 0]), np.array([0, 1, 1]), np.array([1, 0, 1])]
# f = np.array([2, 3, 4])
pos = "700_800"
f, b = wave_form_to_restore.mariorgams[pos], [fki[pos] for fki in wave_form_to_restore.fk]
# 1. Ортогонализация базиса, оставляя первый вектор неизменным
bort = gram_schmidt_with_fixed_first_vector(b)
print("Ортогонализованный базис (bort):")
for vec in bort:
    print(vec)

# 2. Разложение вектора f по ортогональному базису bort
f_bort = decompose_vector(f, bort)
print("\nКоэффициенты разложения в ортогональном базисе (f_bort):", f_bort)

# 3. Найти коэффициенты f_b из равенства f_b * b = f_bort * bort
f_b = find_coefficients_in_original_basis(b, bort, f_bort)
print("\nКоэффициенты разложения в исходном базисе (f_b):", f_b)

# Проверка, что f_b * b = f
reconstructed_f = np.sum([f_b[i] * b[i] for i in range(len(b))], axis=0)
print("\nВектор, восстановленный из коэффициентов и исходного базиса (reconstructed_f):", reconstructed_f)
print("\nИсходный вектор (f):", f)
print("Равенство reconstructed_f и f:", np.sum(reconstructed_f - f))
