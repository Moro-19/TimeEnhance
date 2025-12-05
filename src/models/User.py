class User:
    def __init__(self, UserID, Username, Password, Email, TotalXP=0, TotalTimeCoins=0):
        self.UserID = UserID
        self.Username = Username
        self.Password = Password
        self.Email = Email
        self.TotalXP = TotalXP
        self.TotalTimeCoins = TotalTimeCoins