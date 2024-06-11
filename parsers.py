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
# │   ├── wave_files/              # Результаты моделирования
# │   │   ├── base/
# │   │   │   ├── set1/
# │   │   │   │   ├── wave1.wave
# │   │   │   │   ├── wave2.wave
# │   │   │   │   └── ...
# │   │   │   ├── set2/
# │   │   │   │   ├── wave1.wave
# │   │   │   │   ├── wave2.wave
# │   │   │   │   └── ...
# │   │   │   └── ...
# │   │   │
# │   │   └── experimental/
# │   │       ├── wave1.wave
# │   │       ├── wave2.wave
# │   │       └── ...
# │   │
# │   └── mareograms/              # Мариограммы, полученные из .wave файлов
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


class ParserExperimental:
    def __init__(self):
        pass

    def get_experimental_positions(self, name):
        pass

    def get_experimental_init(self, name):
        pass

    def get_experimental_mariogramm(self,name, pos):
        pass

class ParserBase:

    def __init__(self):
        pass

    def get_bases_names(self):
        pass

    def get_sets_names(self, base_name):
        pass





