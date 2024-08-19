#структура файлов:
# tsunami_simulation/
# │
# ├── config/
# │   └── settings.json  # Настройки для всех моделирований (сопоставление base set -> коофиценты перед condition)
# │
# ├── initial_conditions/
# │   ├── base/                    # Базисные начальные условия
# │   │   ├── set1/
# │   │   │   ├── condition1/
# │   │   │   │   ├── parameters.json
# │   │   │   │   └── data.dat
# │   │   │   ├── condition2/
# │   │   │   │   ├── parameters.json
# │   │   │   │   └── data.dat
# │   │   │   └── ...
# │   │   ├── set2/
# │   │   │   ├── condition1/
# │   │   │   │   ├── parameters.json
# │   │   │   │   └── data.dat
# │   │   │   ├── condition2/
# │   │   │   │   ├── parameters.json
# │   │   │   │   └── data.dat
# │   │   │   └── ...
# │   │   └── ...
# │   │
# │   └── experimental/            # Экспериментальные начальные условия
# │       ├── experiment1/
# │       │   ├── parameters.json
# │       │   └── data.dat
# │       ├── experiment2/
# │       │   ├── parameters.json
# │       │   └── data.dat
# │       └── ...
# │
# ├── results/
# │   ├── mareograms/              # Мариограммы, полученные из .wave файлов
# │       ├── base/
# │       │   ├── set1/
# │       │   │   ├── x1_y1.csv
# │       │   │   ├── x2_y2.csv
# │       │   │   └── ...
# │       │   ├── set2/
# │       │   │   ├── x1_y1.csv
# │       │   │   ├── x2_y2.csv
# │       │   │   └── ...
# │       │   └── ...
# │       │
# │       └── experimental/
# │           ├── exp1/
# │           │   ├── x1_y1.csv
# │           │   ├── x2_y2.csv
# │           │   └── ...
# │           ├── exp2/
# │           │   ├── x1_y1.csv
# │           │   ├── x2_y2.csv
# │           │   └── ...
# │           └── ...
# │
# └──

import json
import os
import glob


class Condition:
    """Класс для управления отдельным начальным условием."""

    def __init__(self, condition_path):
        self.condition_path = condition_path

    def load_json(self):
        """Загружает параметры из JSON файла."""
        json_path = os.path.join(self.condition_path, "parameters.json")
        with open(json_path, 'r') as file:
            parameters = json.load(file)
        return parameters

    def load_dat(self):
        """Загружает данные из .dat файла."""
        dat_path = os.path.join(self.condition_path, "data.dat")
        data = []
        with open(dat_path, 'r') as file:
            for line in file:
                data.append(line.strip())  # Удаляем символы новой строки
        return data


class ConditionSet:
    """Класс для управления набором начальных условий."""

    def __init__(self, directory):
        self.directory = directory

    def list_conditions(self):
        """Возвращает список экземпляров Condition для каждого условия в директории."""
        return [Condition(os.path.join(self.directory, name))
                for name in os.listdir(self.directory)
                if os.path.isdir(os.path.join(self.directory, name))]


class Mareogram:
    """Класс для управления мариограммами, полученными в результате моделирования."""

    def __init__(self, directory):
        self.directory = directory

    def read_mareogram(self, coord):
        """Читает данные мариограммы из CSV файла, соответствующего координатам."""
        file_path = os.path.join(self.directory, f"{coord}.csv")
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                data.append(line.strip())  # Читаем и удаляем символы новой строки
        return data


class Experiment:
    """Класс для управления экспериментом, который включает начальные условия и мариограммы."""

    def __init__(self, base_directory, condition_set_directory, mareogram_directory):
        self.condition_set = ConditionSet(os.path.join(base_directory, condition_set_directory))
        self.mareogram_directory = os.path.join(base_directory, mareogram_directory)
        self.mareograms = self._load_mareograms()

    def _load_mareograms(self):
        """Загружает все мариограммы из директории мариограмм."""
        mareograms = {}
        for file_path in glob.glob(os.path.join(self.mareogram_directory, '*.csv')):
            coord = os.path.splitext(os.path.basename(file_path))[0]
            mareograms[coord] = Mareogram(self.mareogram_directory).read_mareogram(coord)
        return mareograms

    def list_mareograms(self):
        """Возвращает список доступных мариограмм."""
        return list(self.mareograms.keys())

    def get_conditions(self):
        """Возвращает список всех начальных условий в эксперименте с их данными."""
        return [(cond.load_json(), cond.load_dat()) for cond in self.condition_set.list_conditions()]


# Пример использования
if __name__ == "__main__":
    experiment = Experiment('path/to/experiments', 'experimental/condition_set1', 'mareograms/exp1')

    # Вывод списка мариограмм
    print("Available Mareograms:", experiment.list_mareograms())

    # Вывод данных мариограммы для конкретных координат
    for coord, data in experiment.mareograms.items():
        print(f"Mareogram Data for {coord}: {data[:5]}")  # Вывод первых 5 строк данных для примера

    # Получение и вывод начальных условий
    conditions = experiment.get_conditions()
    for json_data, dat_data in conditions:
        print("JSON Data:", json_data)




