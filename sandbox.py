import os
import numpy as np


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


# Пример использования
def find_wave_file(directory):
    """Ищет и возвращает путь к файлу с расширением .wave в указанной директории."""
    for filename in os.listdir(directory):
        if filename.endswith('.wave'):
            return os.path.join(directory, filename)
    raise FileNotFoundError("Файл с расширением .wave не найден.")


# Используем класс HeightMap
directory_path = 'data/quadro/1'  # Укажите путь к директории
wave_file = find_wave_file(directory_path)

# Создаём экземпляр класса HeightMap с шагом 2 (например)
height_map = HeightMap(wave_file, stride=2)

# Получаем значение на определённых координатах
value = height_map.get_value(1, 1)
print(f"Значение на координатах (1, 1) с учётом страйда: {value}")

# Получаем субдискретизированную карту высот
subsampled_map = height_map.get_subsampled_map()
print("Субдискретизированная карта высот:")
print(subsampled_map)
