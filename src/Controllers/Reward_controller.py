from flask import Blueprint, session, redirect, url_for, flash
from Repositories.Task_repo import TaskRepository
from Models.Reward import Reward
import uuid

reward_bp = Blueprint('reward', __name__, url_prefix='/rewards')
task_repo = TaskRepository()

@reward_bp.route('/assign/<task_id>', methods=['POST'])
def assign_reward(task_id):
    user_id = session.get('user_id')
    
    tasks = task_repo.get_tasks_for_user(user_id)
    task = next((t for t in tasks if t.TaskID == task_id), None)
    
    if not task:
        flash('Task not found')
        return redirect(url_for('task.view_tasks', user_id=user_id))
    
    if task.Difficulty.lower() == 'easy':
        xp_amount = 25
        coin_amount = 5
    elif task.Difficulty.lower() == 'medium':
        xp_amount = 50
        coin_amount = 10
    elif task.Difficulty.lower() == 'hard':
        xp_amount = 100
        coin_amount = 20
    
    reward = Reward(
        RewardID=str(uuid.uuid4()),
        XP_amount=xp_amount,
        CoinAmount=coin_amount
    )
    
    flash(f'Reward assigned to task: {xp_amount} XP, {coin_amount} Coins')
    return redirect(url_for('task.view_tasks', user_id=user_id))