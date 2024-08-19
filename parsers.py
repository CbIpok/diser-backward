import numpy as np
import os


def count_numbered_folders(directory):
    numbered_folders = []

    for folder_name in os.listdir(directory):
        # Проверяем, является ли имя папки числом
        if folder_name.isdigit():
            numbered_folders.append(int(folder_name))

    if numbered_folders:
        return max(numbered_folders)
    else:
        return 0  # Если нет пронумерованных папок


def read_mar(file_name):
    file = open(file_name, 'r')
    mar = []
    for line in file.readlines():
        try:
            mar.append(float(line))
        except Exception:
            pass
    return np.array(mar)


def read_mar_folder(folder_name):
    mariograms = {}
    files = os.listdir(folder_name)
    for file in files:
        x = int(file.split("_")[-2])
        y = int(file.split("_")[-1])
        mar = read_mar(f"{folder_name}/{file}")
        mariograms[f"{x}_{y}"] = mar
    return mariograms


class WaveFormToRestore:
    def __init__(self, basis_name, wave_name):
        self.answers = list(map(int, wave_name.split("_")))
        self.mariorgams = read_mar_folder(f"data/{basis_name}/wave_forms/{wave_name}")
        self.fk = [read_mar_folder(f"data/{basis_name}/{i}") for i in
                   range(1, count_numbered_folders(f"data/{basis_name}") + 1)]
        self.coords = self.create_coordinate_list_from_files(f"data/{basis_name}/wave_forms/{wave_name}")

    def extract_coordinates_from_filename(self,filename):
        # Разделяем имя файла на части по символу "_"
        parts = filename.split('_')

        if len(parts) < 3:
            return None  # Если формат имени файла не соответствует ожидаемому, пропускаем его

        try:
            # Последние два элемента parts должны быть координатами x и y
            x = int(parts[-2])
            y = int(parts[-1])
            return (x, y)
        except ValueError:
            return None  # Если не удается преобразовать координаты в числа, пропускаем этот файл

    def create_coordinate_list_from_files(self, directory):
        coordinate_list = []

        # Получаем список всех файлов в директории
        for filename in os.listdir(directory):
            # Извлекаем координаты из имени файла
            coordinates = self.extract_coordinates_from_filename(filename)
            if coordinates:
                coordinate_list.append(coordinates)

        return coordinate_list


