class Inventory:
    def __init__(self, InventoryID, UserID, ItemID, Status="unequipped"):
        self.InventoryID = InventoryID
        self.UserID = UserID
        self.ItemID = ItemID
        self.Status = Status