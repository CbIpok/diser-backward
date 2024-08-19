from parsers import WaveFormToRestore
import restore
import matplotlib.pyplot as plt
import numpy as np

wave = WaveFormToRestore("octo", "1_2_3_4_5_6")
times = [restore.get_restore_time(wave, f"{pos[0]}_{pos[1]}", 95) for pos in wave.coords]
print(times)
x_coords = [c[0] for c in wave.coords]
y_coords = [c[1] for c in wave.coords]
values = times
grid_x, grid_y = np.meshgrid(np.unique(x_coords), np.unique(y_coords))

# Интерполируем значения на сетке
grid_z = np.array(values).reshape(len(np.unique(y_coords)), len(np.unique(x_coords)))

# Создаем 3D-график
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Создаем поверхность
surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis')

# Добавляем цветовую шкалу
fig.colorbar(surf, ax=ax, label='Height Value')

# Подписи осей
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Height Value')
ax.set_title('3D Height Map')

# Показать график
plt.show()