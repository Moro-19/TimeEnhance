import csv

class FileManager:
    _instance = None

    @staticmethod
    def get_instance():
        if FileManager._instance is None:
            FileManager()
        return FileManager._instance

    def __init__(self):
        if FileManager._instance is not None:
            raise Exception("Singleton - use get_instance()")
        else:
            FileManager._instance = self

    def read_csv(self, file_path):
        rows = []
        try:
            with open(file_path, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            return []
        return rows

    def write_csv(self, file_path, rows):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)