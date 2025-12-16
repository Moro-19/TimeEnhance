import sys
import os
import pytest

tests_folder = os.path.dirname(__file__)
project_root = os.path.join(tests_folder, '..')
src_folder = os.path.join(project_root, 'src')
full_src_path = os.path.abspath(src_folder)
sys.path.insert(0, full_src_path)

from Core.Repository_factory import RepositoryFactory
from Repositories.User_repo import UserRepository
from Repositories.Task_repo import TaskRepository
from Repositories.Inventory_repo import InventoryRepository
from Repositories.StoreItem_repo import ItemRepository


class TestRepositoryFactory:
    def test_factory_returns_user_repository(self):
        repo = RepositoryFactory.get_repository("user")
        assert isinstance(repo, UserRepository)
    
    def test_factory_returns_task_repository(self):
        repo = RepositoryFactory.get_repository("task")
        assert isinstance(repo, TaskRepository)
    
    def test_factory_returns_inventory_repository(self):
        repo = RepositoryFactory.get_repository("inventory")
        assert isinstance(repo, InventoryRepository)
    
    def test_factory_returns_item_repository(self):
        repo = RepositoryFactory.get_repository("item")
        assert isinstance(repo, ItemRepository)
    
    def test_factory_returns_item_repository_alt_name(self):
        repo = RepositoryFactory.get_repository("storeitem")
        assert isinstance(repo, ItemRepository)
    
    def test_factory_case_insensitive(self):
        repo_lower = RepositoryFactory.get_repository("user")
        repo_upper = RepositoryFactory.get_repository("USER")
        repo_mixed = RepositoryFactory.get_repository("UsEr")
        
        assert isinstance(repo_lower, UserRepository)
        assert isinstance(repo_upper, UserRepository)
        assert isinstance(repo_mixed, UserRepository)
    
    def test_factory_invalid_type_raises_error(self):
        with pytest.raises(ValueError) as exc_info:
            RepositoryFactory.get_repository("unknown")
        
        assert "Unknown repository type" in str(exc_info.value)
    
    def test_factory_empty_string_raises_error(self):
        with pytest.raises(ValueError):
            RepositoryFactory.get_repository("")
    
    def test_factory_returns_different_instances(self):
        repo1 = RepositoryFactory.get_repository("user")
        repo2 = RepositoryFactory.get_repository("user")
        
        assert repo1 is not repo2