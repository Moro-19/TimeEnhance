import sys
import os

tests_folder = os.path.dirname(__file__)
project_root = os.path.join(tests_folder, '..')
src_folder = os.path.join(project_root, 'src')
full_src_path = os.path.abspath(src_folder)
sys.path.insert(0, full_src_path)

from unittest.mock import MagicMock, patch
from Models.User import User
from Models.Task import Task
from Models.StoreItem import StoreItem

class TestUserController:
    @patch("Controllers.User_controller.user_repo")
    def test_login_route_get(self, mock_repo, client):
        response = client.get('/users/login')
        
        assert response.status_code == 200
    
    @patch("Controllers.User_controller.user_repo")
    def test_view_profile_route(self, mock_repo, client):
        mock_user = User("user1", "testuser", "hash", "test@test.com", 150, 50)
        mock_repo.get_all_users.return_value = [mock_user]
        
        response = client.get('/users/user1/profile')
        
        assert response.status_code == 200


class TestTaskController:
    @patch("Controllers.Task_controller.task_repo")
    def test_view_tasks_route(self, mock_repo, client):
        mock_tasks = [
            Task("task1", "Lab 9", "Testing", "medium", "pending"),
            Task("task2", "Lab 10", "CI/CD", "hard", "pending")
        ]
        mock_repo.get_tasks_for_user.return_value = mock_tasks
        
        response = client.get('/tasks/user1')

        assert response.status_code == 200
    
    @patch("Controllers.Task_controller.task_repo")
    def test_create_task_route_get(self, mock_repo, client):
        response = client.get('/tasks/create')
        
        assert response.status_code == 200


class TestStoreController:
    @patch("Controllers.StoreItem_controller.item_repo")
    @patch("Controllers.StoreItem_controller.user_repo")
    @patch("Controllers.StoreItem_controller.inventory_repo")
    def test_view_store_route_without_session(self, mock_inv_repo, mock_user_repo, mock_item_repo, client):
        mock_items = [
            StoreItem("item1", "Cool Avatar", "100", "Description"),
            StoreItem("item2", "Epic Badge", "200", "Description")
        ]
        mock_item_repo.get_store_items.return_value = mock_items
        mock_user_repo.get_all_users.return_value = []
        mock_inv_repo.get_user_inventory.return_value = []

        response = client.get('/store/')
        
        assert response.status_code == 200


class TestInventoryController:
    @patch("Controllers.Inventory_controller.inventory_repo")
    @patch("Controllers.Inventory_controller.item_repo")
    def test_view_inventory_route(self, mock_item_repo, mock_inv_repo, client):
        mock_inv_repo.get_user_inventory.return_value = []
        mock_item_repo.get_store_items.return_value = []
        
        response = client.get('/inventory/user1')
        
        assert response.status_code == 200


class TestRewardController:
    @patch("Controllers.Reward_controller.task_repo")
    def test_assign_reward_route_without_session(self, mock_repo, client):
        mock_repo.get_tasks_for_user.return_value = []
        
        response = client.post('/rewards/assign/task1', follow_redirects=False)
        
        assert response.status_code in [200, 302, 404]


class TestHomeRoute:
    def test_home_route(self, client):
        response = client.get('/')
        
        assert response.status_code == 200
        assert b"Welcome to Time Enhance!" in response.data