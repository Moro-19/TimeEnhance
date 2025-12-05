from Models.Inventory import Inventory
from Utils.File_manager import FileManager

class InventoryRepository:
    FILE_PATH = "Data/inventory.csv"

    def __init__(self):
        self.file_manager = FileManager.get_instance()

    def get_user_inventory(self, user_id):
        rows = self.file_manager.read_csv(self.FILE_PATH)
        items = []

        for row in rows:
            if row[1] == str(user_id):
                items.append(Inventory(
                    InventoryID=row[0],
                    UserID=row[1],
                    ItemID=row[2],
                    Status=row[3]
                ))

        return items

    def add_to_inventory(self, inventory_item: Inventory):
        rows = self.file_manager.read_csv(self.FILE_PATH)

        rows.append([
            inventory_item.InventoryID,
            inventory_item.UserID,
            inventory_item.ItemID,
            inventory_item.Status
        ])

        self.file_manager.write_csv(self.FILE_PATH, rows)

    def update_item_status(self, inventory_id, new_status):
        rows = self.file_manager.read_csv(self.FILE_PATH)

        for row in rows:
            if row[0] == str(inventory_id):
                row[3] = new_status 

        self.file_manager.write_csv(self.FILE_PATH, rows)
