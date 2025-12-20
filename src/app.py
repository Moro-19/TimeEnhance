from flask import Flask, render_template, session, redirect, url_for
from Controllers.User_controller import user_bp
from Controllers.Task_controller import task_bp
from Controllers.StoreItem_controller import store_bp
from Controllers.Inventory_controller import inventory_bp
from Controllers.Reward_controller import reward_bp
from Repositories.User_repo import UserRepository
from Repositories.Task_repo import TaskRepository
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'supersecretkey'

app.register_blueprint(user_bp)
app.register_blueprint(task_bp)
app.register_blueprint(store_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(reward_bp)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    user_repo = UserRepository()
    task_repo = TaskRepository()
    
    users = user_repo.get_all_users()
    user = next((u for u in users if u.UserID == session['user_id']), None)
    
    if not user:
        session.clear()
        return redirect(url_for('user.login'))
    
    total_xp = int(user.TotalXP) if user.TotalXP else 0
    level = 1
    xp_required = 100
    xp_accumulated = 0
    
    while total_xp >= xp_accumulated + xp_required:
        xp_accumulated += xp_required
        level += 1
        xp_required += 50
    
    current_level_xp = total_xp - xp_accumulated
    xp_for_next_level = xp_required - current_level_xp
    progress_percentage = int((current_level_xp / xp_required) * 100) if xp_required > 0 else 0
    
    tasks = task_repo.get_tasks_for_user(session['user_id'])
    completed_tasks = len([t for t in tasks if t.Status == 'completed'])
    
    return render_template('dashboard.html',
                         user=user,
                         level=level,
                         progress_percentage=progress_percentage,
                         xp_for_next_level=xp_for_next_level,
                         current_level_xp=current_level_xp,
                         completed_tasks=completed_tasks)

if __name__ == '__main__':
    app.run(debug=True)