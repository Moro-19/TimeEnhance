from Models.Task import Task
from Utils.File_manager import FileManager

class TaskRepository:
    FILE_PATH = "Data/tasks.csv"

    def __init__(self):
        self.file_manager = FileManager.get_instance()

    def get_tasks_for_user(self, user_id):
      rows = self.file_manager.read_csv(self.FILE_PATH)
      tasks = []
      for row in rows:
        if row[1] == str(user_id):

            tasks.append(Task(
                TaskID=row[0],
                Title=row[2],
                Description=row[3],
                Difficulty=row[4],
                Status=row[5]
            ))
      return tasks

    def save_task(self, task, user_id):
        rows = self.file_manager.read_csv(self.FILE_PATH)
        rows.append([
            task.TaskID,
            user_id,
            task.Title,
            task.Description,
            task.Difficulty,
            task.Status,
        ])
        self.file_manager.write_csv(self.FILE_PATH, rows)

    def update_task_status(self, task_id, new_status):
        rows = self.file_manager.read_csv(self.FILE_PATH)
        for row in rows:
            if row[0] == str(task_id):
                row[5] = new_status
        self.file_manager.write_csv(self.FILE_PATH, rows)