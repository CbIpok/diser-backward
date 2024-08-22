from parsers import WaveFormToRestore
import restore
import matplotlib.pyplot as plt
import numpy as np
import json


def plot_data(experiment_data):
    x_coords = [c[0] for c in experiment_data["coords"]]
    y_coords = [c[1] for c in experiment_data["coords"]]

    # Создаем 3D-график
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Рисуем точки
    scatter = ax.scatter(x_coords, y_coords, experiment_data["times"], c=experiment_data["times"], cmap='viridis',
                         s=100)

    # Добавляем цветовую шкалу
    fig.colorbar(scatter, ax=ax, label='Height Value')

    # Подписи осей
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Height Value')
    ax.set_title('3D Height Map with Points')

    # Показать график
    plt.show()

def interactive_plot(experiment_data):
    x_coords = [c[0] for c in experiment_data["coords"]]
    y_coords = [c[1] for c in experiment_data["coords"]]
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Рисуем точки
    scatter = ax.scatter(x_coords, y_coords, experiment_data["times"], c=experiment_data["times"], cmap='viridis', s=100)

    # Подписи осей
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Height Value')
    ax.set_title('3D Height Map with Points')

    # Функция обработчика кликов
    def on_click(event):
        # Получаем координаты клика на экране
        if event.inaxes == ax:
            # Трансформируем экранные координаты в координаты на графике
            x_click, y_click = event.xdata, event.ydata
            z_click = None

            # Проходим по всем точкам и проверяем, находится ли клик вблизи одной из них
            min_dist = float('inf')
            closest_point = None

            for i in range(len(x_coords)):
                # Трансформируем 3D координаты в 2D экранные
                screen_coords = ax.transData.transform((x_coords[i], y_coords[i]))
                dist = (screen_coords[0] - x_click) ** 2 + (screen_coords[1] - y_click) ** 2

                if dist < min_dist:
                    min_dist = dist
                    closest_point = (x_coords[i], y_coords[i], 0)

            if closest_point:
                print(f"Clicked on point: (x: { event.xdata}, y: {event.ydata}, z: {closest_point[2]})")

    # Подключаем обработчик кликов
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()


def show_times(basis_name, experiment_name):
    with open(f"data/experiment_dictionary.json", 'r') as file:
        experiment_dictionary = json.load(file)
        experiment_data = experiment_dictionary[basis_name][experiment_name]
        interactive_plot(experiment_data)



# "octo", "1_2_3_4_5_6"
# "octo", "1_2_4_4_2_1"
# "octo", "1_2_4_8_16_32"
# "quadro", "8_4_0_-4"
# "quadro", "1_2_4_8"
show_times("quadro", "8_4_0_-4")
