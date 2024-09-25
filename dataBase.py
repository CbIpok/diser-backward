import sqlite3


class FileDatabase:
    def __init__(self, db_path='file_database.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        """Создает таблицу для хранения файлов, если она еще не существует"""
        query = """
        CREATE TABLE IF NOT EXISTS files (
            bath TEXT,
            wave TEXT,
            txt_file BLOB,
            nc_file BLOB,
            PRIMARY KEY (bath, wave)
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_files(self, bath, wave, txt_file_path, nc_file_path):
        """Сохраняет файлы по ключам bath и wave"""
        with open(txt_file_path, 'rb') as txt_file, open(nc_file_path, 'rb') as nc_file:
            txt_data = txt_file.read()
            nc_data = nc_file.read()

        query = """
        INSERT OR REPLACE INTO files (bath, wave, txt_file, nc_file)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(query, (bath, wave, txt_data, nc_data))
        self.conn.commit()

    def load_files(self, bath, wave, txt_output_path, nc_output_path):
        """Загружает файлы по ключам bath и wave и сохраняет их на диск"""
        query = """
        SELECT txt_file, nc_file FROM files WHERE bath = ? AND wave = ?
        """
        cursor = self.conn.execute(query, (bath, wave))
        result = cursor.fetchone()

        if result:
            txt_data, nc_data = result
            with open(txt_output_path, 'wb') as txt_output, open(nc_output_path, 'wb') as nc_output:
                txt_output.write(txt_data)
                nc_output.write(nc_data)
            print(f"Files saved to {txt_output_path} and {nc_output_path}")
        else:
            print(f"No files found for bath={bath} and wave={wave}")

    def delete_files(self, bath, wave):
        """Удаляет файлы по ключам bath и wave"""
        query = "DELETE FROM files WHERE bath = ? AND wave = ?"
        self.conn.execute(query, (bath, wave))
        self.conn.commit()

    def list_combinations(self):
        """Возвращает список всех комбинаций bath и wave в базе данных"""
        query = "SELECT bath, wave FROM files"
        cursor = self.conn.execute(query)
        combinations = cursor.fetchall()  # Получаем все строки в виде списка кортежей
        return combinations

    def close(self):
        """Закрывает соединение с базой данных"""
        self.conn.close()


# Пример использования
if __name__ == "__main__":
    db = FileDatabase("c:/vm_share/set_2.db")
    print(*db.list_combinations(),sep="\n")

