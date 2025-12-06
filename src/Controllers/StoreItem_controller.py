from flask import Blueprint, session, redirect, url_for, render_template, flash
from Repositories.StoreItem_repo import ItemRepository
from Repositories.Inventory_repo import InventoryRepository
from Repositories.User_repo import UserRepository
from Models.Inventory import Inventory
import uuid

store_bp = Blueprint('store', __name__, url_prefix='/store')
item_repo = ItemRepository()
inventory_repo = InventoryRepository()
user_repo = UserRepository()

@store_bp.route('/')
def view_items():
    user_id = session.get('user_id')
    items = item_repo.get_store_items()
    
    users = user_repo.get_all_users()
    user = next((u for u in users if u.UserID == user_id), None)
    
    inventory = inventory_repo.get_user_inventory(user_id)
    owned_ids = [inv.ItemID for inv in inventory]
    
    return render_template('store.html', 
                         items=items, 
                         user=user, 
                         owned_ids=owned_ids)

@store_bp.route('/purchase/<item_id>', methods=['POST'])
def purchase_item(item_id):
    user_id = session.get('user_id')
    items = item_repo.get_store_items()
    item = next((i for i in items if i.ItemID == item_id), None)
    
    if not item:
        flash('Item not found')
        return redirect(url_for('store.view_items'))
    
    users = user_repo.get_all_users()
    user = next((u for u in users if u.UserID == user_id), None)
    
    inventory = inventory_repo.get_user_inventory(user_id)
    if any(inv.ItemID == item_id for inv in inventory):
        flash('Item already owned')
        return redirect(url_for('store.view_items'))
    
    if user.TotalTimeCoins >= int(item.ItemPrice):
        user.TotalTimeCoins -= int(item.ItemPrice)
        new_inventory = Inventory(
            InventoryID=str(uuid.uuid4()),
            UserID=user_id,
            ItemID=item_id,
            Status='unequipped'
        )
        inventory_repo.add_to_inventory(new_inventory)
        
        flash(f'Successfully purchased {item.ItemName}!')
    else:
        coins_needed = int(item.ItemPrice) - user.TotalTimeCoins
        flash(f'Not enough coins! You need {coins_needed} more coins.')
    
    return redirect(url_for('store.view_items'))