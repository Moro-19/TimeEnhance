from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from Repositories.User_repo import UserRepository
from Repositories.Task_repo import TaskRepository
from Repositories.Inventory_repo import InventoryRepository
from Repositories.StoreItem_repo import ItemRepository
import hashlib

user_bp = Blueprint('user', __name__, url_prefix='/users')
user_repo = UserRepository()
task_repo = TaskRepository()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = user_repo.get_all_users()
        
        for user in users:
            if user.Username == username and user.Password == hash_password(password):
                session['user_id'] = user.UserID
                session['username'] = user.Username
                flash('Login successful!')
                return redirect('/')
            
        flash('Invalid username or password')

    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    session.clear()
    flash('Logged out successfully')
    return redirect(url_for('user.login'))

@user_bp.route('/<user_id>/profile')
def view_profile(user_id):
    users = user_repo.get_all_users()
    user = next((u for u in users if u.UserID == user_id), None)
    
    if not user:
        return render_template('profile.html', user=None, level=0)
    
    total_xp = user.TotalXP
    level = 1
    xp_required = 100  
    xp_accumulated = 0 
    
    while total_xp >= xp_accumulated + xp_required:
        xp_accumulated += xp_required
        level += 1
        xp_required += 50  

    current_level_xp = total_xp - xp_accumulated  
    xp_for_next_level = xp_required - current_level_xp  
    progress_percentage = int((current_level_xp / xp_required) * 100)
    
    return render_template('profile.html', 
                         user=user, 
                         level=level,
                         current_level_xp=current_level_xp,
                         xp_for_next_level=xp_for_next_level,
                         progress_percentage=progress_percentage)

@user_bp.route('/<user_id>/tasks')
def view_tasks(user_id):
    tasks = task_repo.get_tasks_for_user(user_id)
    return render_template('task_list.html', tasks=tasks, user_id=user_id)

@user_bp.route('/<user_id>/rewards')
def view_rewards(user_id):
    inventory_repo = InventoryRepository()
    item_repo = ItemRepository()
    
    users = user_repo.get_all_users()
    user = next((u for u in users if u.UserID == user_id), None)
    
    inventory = inventory_repo.get_user_inventory(user_id)
    items = item_repo.get_store_items()
    
    purchased_items = []
    for inv in inventory:
        item = next((i for i in items if i.ItemID == inv.ItemID), None)
        if item:
            purchased_items.append({'item': item, 'status': inv.Status})
    
    return render_template('rewards.html', user=user, items=purchased_items)