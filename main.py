# This is a sample Python script.
import numpy as np

import dataBase
import nc
from check_points import coords
from restore import approximate_with_non_orthogonal_basis
from sandbox2 import Basis, Wave
import restore
import matplotlib.pyplot as plt
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def calculate_deviations(x, y):
    # Среднеквадратичное отклонение
    mean_squared_deviation = np.sqrt(np.mean((np.array(y) - x) ** 2))

    # Максимальное отклонение по модулю
    max_absolute_deviation = np.max(np.abs(np.array(y) - x))

    return mean_squared_deviation, max_absolute_deviation

def calculate_deviations_pos(x,y):
    db_path = 'c:/vm_share/set_2.db'  # Замените на ваш путь к базе данных
    bath_name = 'data/set_2/bathes/-700_1000_1500.bath'
    basis_pattern = 'square_center_basis_84'
    wave = Wave(bath_name, 0, db_path).get_mariogram(f"{x}_{y}")
    basis = Basis(bath_name, basis_pattern, db_path).get_mariogram(f"{x}_{y}")
    coofs = approximate_with_non_orthogonal_basis(wave, basis)[1]
    # print(Wave(bath_name, 0, db_path).get_size())
    return calculate_deviations(1, coofs)

def calculate_deviations(x,ymin,ymax):
    db_path = 'c:/vm_share/set_2.db'  # Замените на ваш путь к базе данных
    bath_name = 'data/set_2/bathes/-700_1000_1500.bath'
    basis_pattern = 'square_center_basis_84'
    wave = Wave(bath_name, 0, db_path).get_mariogram(f"{x}_{y}")
    basis = Basis(bath_name, basis_pattern, db_path).get_mariogram(f"{x}_{y}")
    coofs = approximate_with_non_orthogonal_basis(wave, basis)[1]
    # print(Wave(bath_name, 0, db_path).get_size())
    return calculate_deviations(1, coofs)

if __name__ == '__main__':
    for x in range(118):
        for y in range(47):
            print(f"x:{x} y:{y} val:{calculate_deviations_pos(x,y)}")

    # coords = [(800, 500), (800, 536), (800, 572), (800, 608), (800, 644), (800, 680), (800, 716), (800, 752), (800, 788), (800, 824), (800, 860), (800, 896), (800, 932), (800, 968), (800, 1004), (800, 1040), (800, 1076), (800, 1112), (800, 1148), (800, 1184), (800, 1220), (800, 1256), (800, 1292), (800, 1328), (836, 500), (836, 536), (836, 572), (836, 608), (836, 644), (836, 680), (836, 716), (836, 752), (836, 788), (836, 824), (836, 860), (836, 896), (836, 932), (836, 968), (836, 1004), (836, 1040), (836, 1076), (836, 1112), (836, 1148), (836, 1184), (836, 1220), (836, 1256), (836, 1292), (836, 1328), (872, 500), (872, 536), (872, 572), (872, 608), (872, 644), (872, 680), (872, 716), (872, 752), (872, 788), (872, 824), (872, 860), (872, 896), (872, 932), (872, 968), (872, 1004), (872, 1040), (872, 1076), (872, 1112), (872, 1148), (872, 1184), (872, 1220), (872, 1256), (872, 1292), (872, 1328), (908, 500), (908, 536), (908, 572), (908, 608), (908, 644), (908, 680), (908, 716), (908, 752), (908, 788), (908, 824), (908, 860), (908, 896), (908, 932), (908, 968), (908, 1004), (908, 1040), (908, 1076), (908, 1112), (908, 1148), (908, 1184), (908, 1220), (908, 1256), (908, 1292), (908, 1328), (944, 500), (944, 536), (944, 572), (944, 608), (944, 644), (944, 680), (944, 716), (944, 752), (944, 788), (944, 824), (944, 860), (944, 896), (944, 932), (944, 968), (944, 1004), (944, 1040), (944, 1076), (944, 1112), (944, 1148), (944, 1184), (944, 1220), (944, 1256), (944, 1292), (944, 1328)]
    # coords = [(0,0),(0,1)]
    # x, y = zip(*coords)
    #
    # # Отобразим точки на графике, где размер и цвет точек зависят от значений в coofs
    # plt.scatter(x, y, c=coofs, cmap='viridis', s=100)
    #
    # # Добавляем цветовую шкалу
    # plt.colorbar(label='Values')
    #
    # # Добавляем подписи осей
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')
    #
    # # Отображаем график
    # plt.title('2D Map of Points')
    # plt.grid(True)
    # plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
