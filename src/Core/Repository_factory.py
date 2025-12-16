from Repositories.User_repo import UserRepository
from Repositories.Task_repo import TaskRepository
from Repositories.Inventory_repo import InventoryRepository
from Repositories.StoreItem_repo import ItemRepository

class RepositoryFactory:
    @staticmethod
    def get_repository(entity_type: str):
        entity_type = entity_type.lower()
        
        if entity_type == 'user':
            return UserRepository()
        elif entity_type == 'task':
            return TaskRepository()
        elif entity_type == 'inventory':
            return InventoryRepository()
        elif entity_type == 'item' or entity_type == 'storeitem':
            return ItemRepository()
        else:
            raise ValueError(f"Unknown repository type: {entity_type}")