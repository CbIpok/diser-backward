import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
# Открываем nc файл
filename = 'D:/dmitrienkomy/vm/shared/out_1000.nc'

def get_region_size_from_dataset(ds):
    """Получить размеры x и y из Dataset"""
    x_size = ds['x'].size
    y_size = ds['y'].size
    return 0, x_size - 1, 0, y_size - 1  # Например, возвращаем минимальные и максимальные индексы

def get_region_size(nc_file):
    # Открываем NetCDF файл с помощью xarray
    ds = xr.open_dataset(nc_file)

    # Извлекаем переменную height
    height = ds['height']

    # Проверяем, что переменная содержит координаты x и y
    if 'x' not in height.dims or 'y' not in height.dims:
        raise ValueError("Dimensions 'x' or 'y' not found in the dataset.")

    # Получаем координаты x и y
    x_coords = height['x']
    y_coords = height['y']

    # Находим минимальные и максимальные значения для x и y
    x_min = x_coords.min().item()
    x_max = x_coords.max().item()
    y_min = y_coords.min().item()
    y_max = y_coords.max().item()

    return x_min, x_max, y_min, y_max

def extract_height_2d(nc_file, x_index, y_index):
    # Открываем NetCDF файл с помощью xarray
    ds = xr.open_dataset(nc_file)

    # Извлекаем переменную height
    height = ds['height']

    # Проверяем, что измерения x, y и time существуют
    if 'x' not in height.dims or 'y' not in height.dims or 'time' not in height.dims:
        raise ValueError("Dimensions 'x', 'y', or 'time' not found in the dataset.")

    # Извлекаем данные для всех временных шагов по индексу x и y
    height_2d = height.isel(x=x_index, y=y_index)

    return height_2d.values

# for x in [10,20,30,40]:
#     data = extract_height_2d(filename,x,50)
#     plt.plot(data, label = f"{x}" )
# plt.show()

if __name__ == "__main__":
    print(get_region_size(filename))