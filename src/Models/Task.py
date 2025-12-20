class Task:
    def __init__(self, TaskID, Title, Description, Difficulty, Status="pending"):
        self.TaskID = TaskID
        self.Title = Title
        self.Description = Description
        self.Difficulty = Difficulty
        self.Status = Status 