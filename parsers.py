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
    files = [filename for filename in files if not filename.endswith('.wave')]
    for file in files:
        x = int(file.split("_")[-2])
        y = int(file.split("_")[-1])
        mar = read_mar(f"{folder_name}/{file}")
        mariograms[f"{x}_{y}"] = mar
    return mariograms


def find_wave_file(directory):
    """Ищет и возвращает путь к файлу с расширением .wave в указанной директории."""
    for filename in os.listdir(directory):
        if filename.endswith('.wave'):
            return os.path.join(directory, filename)
    raise FileNotFoundError("Файл с расширением .wave не найден.")


class HeightMap:
    def __init__(self, file_path, stride=1):
        self.file_path = file_path
        self.stride = stride
        self.map_data = self._load_map_data()

        # Размеры карты
        self.height = self.map_data.shape[0]
        self.width = self.map_data.shape[1]

    def _load_map_data(self):
        """Загружает данные из файла и возвращает их в виде 2D numpy массива."""
        with open(self.file_path, 'r') as file:
            data = file.read()

        # Преобразуем текст в 2D массив float значений
        lines = data.strip().split('\n')
        map_data = np.array([[float(val) for val in line.split()] for line in lines])

        return map_data

    def get_value(self, x, y):
        """Возвращает значение карты высот с учетом страйда."""
        x_index = x * self.stride
        y_index = y * self.stride

        # Проверка выхода за границы
        if x_index >= self.width or y_index >= self.height:
            raise IndexError("Индекс выходит за пределы карты высот.")

        return self.map_data[y_index, x_index]

    def get_subsampled_map(self):
        """Возвращает 2D массив с учетом страйда."""
        return self.map_data[::self.stride, ::self.stride]


class WaveFormToRestore:
    def __init__(self, basis_name, wave_name):
        self.answers = list(map(int, wave_name.split("_")))
        self.mariorgams = read_mar_folder(f"data/{basis_name}/wave_forms/{wave_name}")
        self.fk = [read_mar_folder(f"data/{basis_name}/{i}") for i in
                   range(1, count_numbered_folders(f"data/{basis_name}") + 1)]
        self.coords = self._create_coordinate_list_from_files(f"data/{basis_name}/wave_forms/{wave_name}")
        self.fk_waves = [HeightMap(find_wave_file(f"data/{basis_name}/{i}"), 2) for i in
                         range(1, count_numbered_folders(f"data/{basis_name}") + 1)]

    @staticmethod
    def _extract_coordinates_from_filename(filename):
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

    def _create_coordinate_list_from_files(self, directory):
        coordinate_list = []

        # Получаем список всех файлов в директории
        for filename in os.listdir(directory):
            # Извлекаем координаты из имени файла
            coordinates = self._extract_coordinates_from_filename(filename)
            if coordinates:
                coordinate_list.append(coordinates)

        return coordinate_list
