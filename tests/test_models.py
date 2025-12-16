import sys
import os

tests_folder = os.path.dirname(__file__)
project_root = os.path.join(tests_folder, '..')
src_folder = os.path.join(project_root, 'src')
full_src_path = os.path.abspath(src_folder)
sys.path.insert(0, full_src_path)

from Models.User import User
from Models.Task import Task
from Models.Reward import Reward
from Models.StoreItem import StoreItem
from Models.Inventory import Inventory


class TestUserModel:
    def test_user_creation(self):
        user = User(
            UserID="1",
            Username="testuser",
            Password="hashedpass123",
            Email="test@example.com",
            TotalXP=100,
            TotalTimeCoins=50
        )
        
        assert user.UserID == "1"
        assert user.Username == "testuser"
        assert user.Password == "hashedpass123"
        assert user.Email == "test@example.com"
        assert user.TotalXP == 100
        assert user.TotalTimeCoins == 50
    
    def test_user_creation_defaults(self):
        user = User(
            UserID="2",
            Username="newuser",
            Password="pass",
            Email="new@example.com"
        )

        assert user.TotalXP == 0
        assert user.TotalTimeCoins == 0

class TestTaskModel:
    def test_task_creation(self):
        task = Task(
            TaskID="task1",
            Title="Complete Lab 9",
            Description="Write unit tests",
            Difficulty="medium",
            Status="pending"
        )
        
        assert task.TaskID == "task1"
        assert task.Title == "Complete Lab 9"
        assert task.Description == "Write unit tests"
        assert task.Difficulty == "medium"
        assert task.Status == "pending"
    
    def test_task_creation_default_status(self):
        task = Task(
            TaskID="task2",
            Title="Study",
            Description="Review notes",
            Difficulty="easy"
        )
        
        assert task.Status == "pending"
    
    def test_task_difficulties(self):
        easy_task = Task("t1", "Easy Task", "Desc", "easy")
        medium_task = Task("t2", "Medium Task", "Desc", "medium")
        hard_task = Task("t3", "Hard Task", "Desc", "hard")
        
        assert easy_task.Difficulty == "easy"
        assert medium_task.Difficulty == "medium"
        assert hard_task.Difficulty == "hard"


class TestRewardModel:
    def test_reward_creation(self):
        reward = Reward(
            RewardID="reward1",
            XP_amount=50,
            CoinAmount=10
        )
        
        assert reward.RewardID == "reward1"
        assert reward.XP_amount == 50
        assert reward.CoinAmount == 10
    
    def test_reward_creation_defaults(self):
        reward = Reward(RewardID="reward2")
        
        assert reward.XP_amount == 0
        assert reward.CoinAmount == 0
    
    def test_reward_amounts(self):
        small = Reward("r1", 25, 5)    # easy task reward
        medium = Reward("r2", 50, 10)  # medium task reward
        large = Reward("r3", 100, 20)  # hard task reward
        
        assert small.XP_amount == 25 and small.CoinAmount == 5
        assert medium.XP_amount == 50 and medium.CoinAmount == 10
        assert large.XP_amount == 100 and large.CoinAmount == 20


class TestStoreItemModel:
    def test_storeitem_creation(self):
        item = StoreItem(
            ItemID="item1",
            ItemName="Cool Avatar",
            ItemPrice="100",
            ItemDescription="A cool avatar"
        )
        
        assert item.ItemID == "item1"
        assert item.ItemName == "Cool Avatar"
        assert item.ItemPrice == "100"
        assert item.ItemDescription == "A cool avatar"
    
    def test_storeitem_various_prices(self):
        cheap = StoreItem("i1", "Cheap Item", "10", "Desc")
        expensive = StoreItem("i2", "Expensive Item", "500", "Desc")
        
        assert cheap.ItemPrice == "10"
        assert expensive.ItemPrice == "500"


class TestInventoryModel:
    def test_inventory_creation(self):
        inv = Inventory(
            InventoryID="inv1",
            UserID="user1",
            ItemID="item1",
            Status="equipped"
        )
        
        assert inv.InventoryID == "inv1"
        assert inv.UserID == "user1"
        assert inv.ItemID == "item1"
        assert inv.Status == "equipped"
    
    def test_inventory_creation_default_status(self):
        inv = Inventory(
            InventoryID="inv2",
            UserID="user2",
            ItemID="item2"
        )
        
        assert inv.Status == "unequipped"
    
    def test_inventory_status_types(self):
        equipped = Inventory("i1", "u1", "it1", "equipped")
        unequipped = Inventory("i2", "u2", "it2", "unequipped")
        
        assert equipped.Status == "equipped"
        assert unequipped.Status == "unequipped"