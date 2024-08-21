import os
from parsers import WaveFormToRestore
import restore
import json
from tqdm import tqdm

threshold = 95


def create_experiment_dict(base_dir):
    experiment_dict = {}

    # Проходим по всем папкам в директории base_dir
    for set_name in os.listdir(base_dir):
        set_path = os.path.join(base_dir, set_name)

        # Проверяем, является ли элемент папкой
        if os.path.isdir(set_path):
            # Путь к папке wave_forms
            wave_forms_path = os.path.join(set_path, 'wave_forms')

            # Проверяем, существует ли папка wave_forms и является ли она директорией
            if os.path.isdir(wave_forms_path):
                # Инициализируем пустой список для названий экспериментов
                experiment_list = []

                # Проходим по всем папкам внутри wave_forms
                for experiment_name in os.listdir(wave_forms_path):
                    experiment_path = os.path.join(wave_forms_path, experiment_name)

                    # Проверяем, является ли элемент папкой (название эксперимента)
                    if os.path.isdir(experiment_path):
                        experiment_list.append(experiment_name)

                # Добавляем список экспериментов в словарь
                experiment_dict[set_name] = experiment_list

    return experiment_dict


def restore_all_times():
    experiment_dict = create_experiment_dict("data")
    restore_res = {}
    for basis in experiment_dict:
        restore_res[basis] = {}
        for experiment in experiment_dict[basis]:
            wave = WaveFormToRestore(basis, experiment)
            times = [restore.get_restore_time(wave, f"{pos[0]}_{pos[1]}", threshold) for pos in
                     tqdm(wave.coords, desc=f"process basis {basis} experiment {experiment}")]
            restore_res[basis][experiment] = {"coords": wave.coords, "times": times}
    output_file = 'data/experiment_dictionary.json'
    # Сохранение словаря в файл JSON
    with open(output_file, 'w') as file:
        json.dump(restore_res, file, indent=4)


# restore_all_times()
