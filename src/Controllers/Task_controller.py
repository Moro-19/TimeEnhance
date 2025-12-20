from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from Repositories.Task_repo import TaskRepository
from Repositories.User_repo import UserRepository
from Models.Task import Task
from Utils.File_manager import FileManager
import uuid

task_bp = Blueprint('task', __name__, url_prefix='/tasks')
task_repo = TaskRepository()
user_repo = UserRepository()

@task_bp.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            flash('Please login first')
            return redirect(url_for('user.login'))
        
        title = request.form.get('title')
        description = request.form.get('description', '')
        difficulty = request.form.get('difficulty', 'medium')
        
        if not title:
            flash('Title is required')
            return render_template('create_task.html')
        
        if difficulty not in ['easy', 'medium', 'hard']:
            flash('Invalid difficulty selected')
            return render_template('create_task.html')
        
        task_id = str(uuid.uuid4())
        task = Task(
            TaskID=task_id, 
            Title=title,
            Description=description,
            Difficulty=difficulty,
            Status='pending'  
        )
        
        task_repo.save_task(task, user_id)
        
        file_manager = FileManager.get_instance()
        reward_rows = file_manager.read_csv("Data/rewards.csv")
        
        if difficulty == 'easy':
            xp, coins = 25, 5
        elif difficulty == 'medium':
            xp, coins = 50, 10
        else:  
            xp, coins = 100, 20
        
        reward_rows.append([task_id, str(xp), str(coins)])
        file_manager.write_csv("Data/rewards.csv", reward_rows)
        
        flash('Task created successfully!')
        return redirect(url_for('task.view_tasks', user_id=user_id))
    
    return render_template('create_task.html')

@task_bp.route('/<user_id>/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(user_id, task_id):
    tasks = task_repo.get_tasks_for_user(user_id)
    task = next((t for t in tasks if t.TaskID == task_id), None)
    
    if not task:
        flash('Task not found')
        return redirect(url_for('task.view_tasks', user_id=user_id))
    
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_description = request.form.get('description', '')
        new_difficulty = request.form.get('difficulty')
        
        file_manager = FileManager.get_instance()
        task_rows = file_manager.read_csv("Data/tasks.csv")
        
        for row in task_rows:
            if row[0] == task_id:
                row[2] = new_title
                row[3] = new_description
                row[4] = new_difficulty
        
        file_manager.write_csv("Data/tasks.csv", task_rows)
        
        reward_rows = file_manager.read_csv("Data/rewards.csv")
        if new_difficulty == 'easy':
            xp, coins = 25, 5
        elif new_difficulty == 'medium':
            xp, coins = 50, 10
        else:
            xp, coins = 100, 20
        
        for row in reward_rows:
            if row[0] == task_id:
                row[1] = str(xp)
                row[2] = str(coins)
        
        file_manager.write_csv("Data/rewards.csv", reward_rows)
        
        flash('Task updated!')
        return redirect(url_for('task.view_tasks', user_id=user_id))
    
    return render_template('edit_task.html', task=task, user_id=user_id)

@task_bp.route('/<user_id>/delete/<task_id>', methods=['POST'])
def delete_task(user_id, task_id):
    file_manager = FileManager.get_instance()
    
    rows = file_manager.read_csv("Data/tasks.csv")
    updated_rows = [row for row in rows if row[0] != task_id]
    file_manager.write_csv("Data/tasks.csv", updated_rows)
    
    reward_rows = file_manager.read_csv("Data/rewards.csv")
    updated_rewards = [row for row in reward_rows if row[0] != task_id]
    file_manager.write_csv("Data/rewards.csv", updated_rewards)
    
    flash('Task deleted!')
    return redirect(url_for('task.view_tasks', user_id=user_id))

@task_bp.route('/<user_id>/complete/<task_id>', methods=['POST'])
def complete_task(user_id, task_id):
    tasks = task_repo.get_tasks_for_user(user_id)
    task = next((t for t in tasks if t.TaskID == task_id), None)
    
    if not task:
        flash('Task not found')
        return redirect(url_for('task.view_tasks', user_id=user_id))
    
    if task.Status == 'completed':
        flash('Task already completed')
        return redirect(url_for('task.view_tasks', user_id=user_id))
    
    task_repo.update_task_status(task_id, 'completed')
    
    file_manager = FileManager.get_instance()
    reward_rows = file_manager.read_csv("Data/rewards.csv")
    
    xp = 0
    coins = 0
    for row in reward_rows:
        if row[0] == task_id:
            xp = int(row[1])
            coins = int(row[2])
            break
    
    user_rows = file_manager.read_csv("Data/users.csv")
    for row in user_rows:
        if row[0] == user_id:
            current_xp = int(row[4])
            current_coins = int(row[5])
            row[4] = str(current_xp + xp)
            row[5] = str(current_coins + coins)
    
    file_manager.write_csv("Data/users.csv", user_rows)
    
    flash(f'Task completed! +{xp} XP, +{coins} Coins')
    return redirect(url_for('task.view_tasks', user_id=user_id))

@task_bp.route('/<user_id>')
def view_tasks(user_id):
    tasks = task_repo.get_tasks_for_user(user_id)
    return render_template('task_list.html', tasks=tasks, user_id=user_id)