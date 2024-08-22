import json

import matplotlib.pyplot as plt
import numpy as np
from restore import evolution
import parsers
# Пример данных

file = open(f"data/experiment_dictionary.json", 'r')
# "octo", "1_2_3_4_5_6"
# "octo", "1_2_4_4_2_1"
# "octo", "1_2_4_8_16_32"
# "quadro", "8_4_0_-4"
# "quadro", "1_2_4_8"
basis = "quadro"
experiment = "8_4_0_-4"
experiment_dictionary = json.load(file)
experiment_data = experiment_dictionary[basis][experiment]
coords = np.array(experiment_data["coords"])
values = experiment_data["times"]
# Создание 2D графика с цветными точками
fig, ax = plt.subplots()
sc = ax.scatter(coords[:, 0], coords[:, 1], c=values, cmap='viridis', s=100)

# Добавление цветовой шкалы
plt.colorbar(sc, label='Height Value')

# Функция-обработчик кликов
def on_click(event):
    # Получаем координаты клика на графике
    if event.inaxes == ax:
        # Определяем ближайшую точку к месту клика
        x_click, y_click = event.xdata, event.ydata
        distances = np.sqrt((coords[:, 0] - x_click)**2 + (coords[:, 1] - y_click)**2)
        min_index = np.argmin(distances)
        # Вызов функции с параметрами ближайшей точки
        evolution(parsers.WaveFormToRestore(basis, experiment), f"{coords[min_index, 0]}_{coords[min_index, 1]}")
        print(f"Clicked on point: (x: {coords[min_index, 0]}, y: {coords[min_index, 1]}, value: {values[min_index]})")


# Подключаем обработчик кликов
fig.canvas.mpl_connect('button_press_event', on_click)

# Показ графика
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('2D Height Map with Clickable Points')
plt.show()
