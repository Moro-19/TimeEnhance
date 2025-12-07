from Models.StoreItem import StoreItem
from Utils.File_manager import FileManager

class ItemRepository:
    FILE_PATH = "Data/items.csv"

    def __init__(self):
        self.file_manager = FileManager.get_instance()

    def get_store_items(self):
        rows = self.file_manager.read_csv(self.FILE_PATH)
        items = []
        for row in rows:
            items.append(StoreItem(*row))
        return items