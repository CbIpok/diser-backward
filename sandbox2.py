import re
import sqlite3
import xarray as xr
from tqdm import tqdm
import io
# import h5netcdf
import nc
# from check_points import coords
# from nc import get_region_size


def get_basis_files(db_path, bath_name, basis_pattern):
    # Открываем соединение с базой данных
    conn = sqlite3.connect(db_path)

    # Формируем запрос для поиска записей с нужным bath и с wave, содержащим указанную подстроку
    query = """
    SELECT bath, wave FROM files WHERE bath = ? AND wave LIKE ?
    """

    # Выполняем запрос
    cursor = conn.execute(query, (bath_name, f"%/{basis_pattern}/%"))
    results = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    return results

def get_region_size_from_dataset(ds):
    """Получить размеры x и y из Dataset"""
    x_size = ds['x'].size
    y_size = ds['y'].size
    return 0, x_size - 1, 0, y_size - 1  # Например, возвращаем минимальные и максимальные индексы

def get_nc_file_by_keys_in_memory(db_path, bath, wave):
    """Получить nc файл по ключам bath и wave, и загрузить его напрямую в память"""
    conn = sqlite3.connect(db_path)

    # SQL-запрос для получения файла по ключам bath и wave
    query = """
    SELECT nc_file FROM files WHERE bath = ? AND wave = ?
    """
    cursor = conn.execute(query, (bath, wave))
    result = cursor.fetchone()

    conn.close()

    if result:
        nc_file_data = result[0]  # Извлекаем бинарные данные файла .nc
        # Используем io.BytesIO для создания файлового объекта в памяти
        return io.BytesIO(nc_file_data)
    else:
        print(f"Файл не найден для bath={bath} и wave={wave}")
        return None

def get_mariogramm(ds,x , y):
    height_data = ds['height']
    return height_data.sel(x=x, y=y).values


def get_mariogramm_range(ds, xo, ymin, ymax):
    # Извлекаем данные о высоте
    height_data = ds['height']

    # Извлекаем диапазон по x = xo и диапазон по y от ymin до ymax
    return height_data.sel(x=xo, y=slice(ymin, ymax)).values

def create_dict_mariograms(x_min, x_max, y_min, y_max, ds, step_x, step_y):
    """Создать словарь с данными для всех комбинаций x и y из загруженного Dataset"""
    result_dict = {}

    # Загрузка данных height в память
    height_data = ds['height'].isel(x=slice(x_min, x_max+1,step_x), y=slice(y_min, y_max+1,step_y)).load()

    # Цикл по всем комбинациям x и y
    for x in tqdm(range(x_min, x_max + 1,step_x)):
        for y in range(y_min, y_max + 1,step_y):
            key = f"{x}_{y}"
            result_dict[key] = height_data.sel(x=x//step_x, y=y//step_y).values

    return result_dict

def get_wave_files(db_path, bath_name):
    """Получить все записи для конкретного bath и директории wave"""
    # Открываем соединение с базой данных
    conn = sqlite3.connect(db_path)

    # Формируем запрос для поиска записей с нужным bath и wave содержащим '/waves/'
    query = """
    SELECT bath, wave FROM files WHERE bath = ? AND wave LIKE ?
    """

    # Выполняем запрос
    cursor = conn.execute(query, (bath_name, "%/waves/%"))
    results = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    return results


def sort_by_wave_number(records):
    # Функция для извлечения числового значения перед ".wave"
    def extract_wave_number(record):
        wave_path = record[1]  # Извлекаем второй элемент кортежа, где находится wave
        # Используем регулярное выражение для поиска числа перед ".wave"
        match = re.search(r'(\d+)\.wave$', wave_path)
        if match:
            return int(match.group(1))  # Возвращаем числовое значение
        return float('inf')  # Если не удалось найти число, помещаем запись в конец

    # Сортируем массив кортежей по числу перед ".wave"
    return sorted(records, key=extract_wave_number)




def create_dict_mariograms_by_keys_in_memory(bath, wave):
    # Получаем nc файл напрямую из БД как объект в памяти
    nc_file_memory = get_nc_file_by_keys_in_memory(db_path, bath, wave)
    if nc_file_memory is None:
        return None

    # Открываем Dataset из памяти
    ds = xr.open_dataset(nc_file_memory, engine='h5netcdf')

    # Извлекаем размер области
    size = nc.get_region_size_from_dataset(ds)  # Вы можете сделать такую функцию для извлечения размеров
    return create_dict_mariograms(*size, ds)

class Wave:
    def __init__(self,bath_name,wave_idx,db_path):
        self.wave_files = sort_by_wave_number(get_wave_files(db_path,bath_name))
        self.wave_keys = self.wave_files[wave_idx]
        self.db_path = db_path

    def get_mariogram(self,coords_str):
        x,y = map(int,coords_str.split("_"))
        ds = xr.open_dataset(get_nc_file_by_keys_in_memory(self.db_path, *self.wave_keys), engine='h5netcdf')
        return get_mariogramm(ds,x,y)

    def get_size(self):
        ds = xr.open_dataset(get_nc_file_by_keys_in_memory(self.db_path, *self.wave_keys), engine='h5netcdf')
        return get_region_size_from_dataset(ds)


class Basis:
    def __init__(self,bath_name,basis_pattern,db_path):
        self.basis_files = sort_by_wave_number(get_basis_files(db_path, bath_name, basis_pattern))
        self.db_path = db_path

    def get_mariogram(self,coords_str):
        mariograms = []
        for keys in self.basis_files:
            x,y = map(int,coords_str.split("_"))
            ds = xr.open_dataset(get_nc_file_by_keys_in_memory(self.db_path, *keys), engine='h5netcdf')
            mariograms.append(get_mariogramm(ds,x,y))
        return mariograms

    def get_mariograms(self,step_x,step_y):
        mariograms = []
        for keys in tqdm(self.basis_files):
            ds = xr.open_dataset(get_nc_file_by_keys_in_memory(self.db_path, *keys), engine='h5netcdf')
            coords = get_region_size_from_dataset(ds)
            mariograms.append(create_dict_mariograms(*coords,ds,step_x,step_y))
        return mariograms

if __name__ == "__main__":
    # Пример использования
    db_path = 'c:/vm_share/set_1.db'  # Замените на ваш путь к базе данных
    bath_name = '/mnt/hgfs/shared/set_1/bathes/2048_100_1000.bath'
    basis_pattern = 'square_center_basis_144'

    basis_files = sort_by_wave_number(get_basis_files(db_path, bath_name, basis_pattern))
    wave_files = sort_by_wave_number(get_wave_files(db_path,bath_name))
    waves_mariograms = [create_dict_mariograms_by_keys_in_memory(*wave_file) for wave_file in wave_files]
    # basis_mariograms = [create_dict_mariograms_by_keys_in_memory(*basis_file) for basis_file in basis_files]
    print(Wave(bath_name,0,db_path).get_mariogram("0_0"))
    print(Basis(bath_name,basis_pattern,db_path).get_mariogram("0_0"))