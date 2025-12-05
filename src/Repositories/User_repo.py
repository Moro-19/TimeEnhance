from Models.User import User
from Utils.File_manager import FileManager

class UserRepository:
    FILE_PATH = "Data/users.csv"

    def __init__(self):
        self.file_manager = FileManager.get_instance()

    def get_all_users(self):
        rows = self.file_manager.read_csv(self.FILE_PATH)
        users = []
        for row in rows:
            users.append(User(*row))
        return users

    def find_by_email(self, email):
        users = self.get_all_users()
        for user in users:
            if user.Email == email:
                return user
        return None

    def save_user(self, user):
        rows = self.file_manager.read_csv(self.FILE_PATH)
        rows.append([
            user.UserID,
            user.Username,
            user.Password,
            user.Email,
            user.TotalXP,
            user.TotalTimeCoins
        ])
        self.file_manager.write_csv(self.FILE_PATH, rows)