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
        title = request.form.get('title')
        description = request.form.get('description', '')
        difficulty = request.form.get('difficulty', 'medium')
        
        if not title:
            flash('Title is required')
            return render_template('create_task.html')
        
        if not difficulty in ['easy', 'medium', 'hard']:
            flash('Invalid difficulty selected')
            return render_template('create_task.html')
        
        task = Task(
            TaskID=str(uuid.uuid4()), 
            Title=title,
            Description=description,
            Difficulty=difficulty,
            Status='pending'  
        )
        
        task_repo.save_task(task, user_id)
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
        task.Title = request.form.get('title')
        task.Description = request.form.get('description', '')
        task.Difficulty = request.form.get('difficulty')
        flash('Task updated!')
        return redirect(url_for('task.view_tasks', user_id=user_id))
    return render_template('edit_task.html', task=task, user_id=user_id)

@task_bp.route('/<user_id>/delete/<task_id>', methods=['POST'])
def delete_task(user_id, task_id):
    file_manager = FileManager.get_instance()
    rows = file_manager.read_csv("Data/tasks.csv")
    updated_rows = [row for row in rows if row[0] != task_id]
    file_manager.write_csv("Data/tasks.csv", updated_rows)
    flash('Task deleted!')
    return redirect(url_for('task.view_tasks', user_id=user_id))

@task_bp.route('/<user_id>/complete/<task_id>', methods=['POST'])
def complete_task(user_id, task_id):
    tasks = task_repo.get_tasks_for_user(user_id)
    task = next((t for t in tasks if t.TaskID == task_id), None)
    
    if task and task.Status != 'completed':
        task_repo.update_task_status(task_id, 'completed')
        
        from Utils.File_manager import FileManager
        file_manager = FileManager.get_instance()
        
        reward_rows = file_manager.read_csv("Data/rewards.csv")
        reward = None
        for row in reward_rows:
            if row[0] == task_id:  
                xp = int(row[1])
                coins = int(row[2])
                reward = True
                break
        
        if reward:
            users = user_repo.get_all_users()
            user = next((u for u in users if u.UserID == user_id), None)
            if user:
                user.TotalXP += xp
                user.TotalTimeCoins += coins
            
            flash(f"Task completed! +{xp} XP, +{coins} Coins")
        else:
            flash('Task completed but no reward found')
    else:
        flash('Task already completed')
    
    return redirect(url_for('task.view_tasks', user_id=user_id))

@task_bp.route('/<user_id>')
def view_tasks(user_id):
    tasks = task_repo.get_tasks_for_user(user_id)
    return render_template('task_list.html', tasks=tasks, user_id=user_id)