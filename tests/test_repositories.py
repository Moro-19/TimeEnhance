import sys
import os

tests_folder = os.path.dirname(__file__)
project_root = os.path.join(tests_folder, '..')
src_folder = os.path.join(project_root, 'src')
full_src_path = os.path.abspath(src_folder)
sys.path.insert(0, full_src_path)

from unittest.mock import MagicMock, patch
from Repositories.User_repo import UserRepository
from Repositories.Task_repo import TaskRepository
from Repositories.Inventory_repo import InventoryRepository
from Repositories.StoreItem_repo import ItemRepository
from Models.User import User
from Models.Task import Task
from Models.Inventory import Inventory
from Models.StoreItem import StoreItem


class TestUserRepository:
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_get_all_users(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = [
            ["1", "alice", "hash123", "alice@test.com", "100", "50"],
            ["2", "bob", "hash456", "bob@test.com", "200", "75"]
        ]
        mock_file_manager.return_value = mock_fm_instance
    
        repo = UserRepository()
        users = repo.get_all_users()
        
        assert len(users) == 2
        assert users[0].Username == "alice"
        assert users[1].Username == "bob"
        assert users[0].TotalXP == "100"
    
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_find_by_email(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = [
            ["1", "alice", "hash123", "alice@test.com", "100", "50"],
            ["2", "bob", "hash456", "bob@test.com", "200", "75"]
        ]
        mock_file_manager.return_value = mock_fm_instance
        
        repo = UserRepository()
        user = repo.find_by_email("bob@test.com")
        
        assert user is not None
        assert user.Username == "bob"
        assert user.Email == "bob@test.com"
    
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_find_by_email_not_found(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = [
            ["1", "alice", "hash123", "alice@test.com", "100", "50"]
        ]
        mock_file_manager.return_value = mock_fm_instance
        
        repo = UserRepository()
        user = repo.find_by_email("nonexistent@test.com")
        
        assert user is None
    
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_save_user(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = []
        mock_file_manager.return_value = mock_fm_instance
        
        repo = UserRepository()
        user = User("3", "charlie", "hash789", "charlie@test.com", 0, 0)
        repo.save_user(user)
        
        mock_fm_instance.write_csv.assert_called_once()


class TestTaskRepository:
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_get_tasks_for_user(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = [
            ["task1", "user1", "Complete Lab 9", "Write tests", "medium", "pending"],
            ["task2", "user2", "Study", "Review notes", "easy", "pending"],
            ["task3", "user1", "Exercise", "Go running", "hard", "completed"]
        ]
        mock_file_manager.return_value = mock_fm_instance
        
        repo = TaskRepository()
        tasks = repo.get_tasks_for_user("user1")
        
        assert len(tasks) == 2
        assert tasks[0].Title == "Complete Lab 9"
        assert tasks[1].Title == "Exercise"
    
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_save_task(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = []
        mock_file_manager.return_value = mock_fm_instance
        
        repo = TaskRepository()
        task = Task("task1", "New Task", "Description", "medium", "pending")
        repo.save_task(task, "user1")
        
        mock_fm_instance.write_csv.assert_called_once()
    
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_update_task_status(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = [
            ["task1", "user1", "Complete Lab 9", "Write tests", "medium", "pending"]
        ]
        mock_file_manager.return_value = mock_fm_instance
        
        repo = TaskRepository()
        repo.update_task_status("task1", "completed")
        
        mock_fm_instance.write_csv.assert_called_once()


class TestInventoryRepository:
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_get_user_inventory(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = [
            ["inv1", "user1", "item1", "equipped"],
            ["inv2", "user2", "item2", "unequipped"],
            ["inv3", "user1", "item3", "unequipped"]
        ]
        mock_file_manager.return_value = mock_fm_instance
        
        repo = InventoryRepository()
        inventory = repo.get_user_inventory("user1")
        
        assert len(inventory) == 2
        assert inventory[0].ItemID == "item1"
        assert inventory[1].ItemID == "item3"
    
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_add_to_inventory(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = []
        mock_file_manager.return_value = mock_fm_instance
        
        repo = InventoryRepository()
        inv_item = Inventory("inv1", "user1", "item1", "unequipped")
        repo.add_to_inventory(inv_item)
        
        mock_fm_instance.write_csv.assert_called_once()


class TestItemRepository:
    @patch("Utils.File_manager.FileManager.get_instance")
    def test_get_store_items(self, mock_file_manager):
        mock_fm_instance = MagicMock()
        mock_fm_instance.read_csv.return_value = [
            ["item1", "Cool Avatar", "100", "A cool avatar"],
            ["item2", "Epic Badge", "200", "An epic badge"]
        ]
        mock_file_manager.return_value = mock_fm_instance
        
        repo = ItemRepository()
        items = repo.get_store_items()
        
        assert len(items) == 2
        assert items[0].ItemName == "Cool Avatar"
        assert items[1].ItemPrice == "200"