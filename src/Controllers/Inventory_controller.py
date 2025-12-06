from flask import Blueprint, session, redirect, url_for, render_template, flash
from Repositories.Inventory_repo import InventoryRepository
from Repositories.StoreItem_repo import ItemRepository

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')
inventory_repo = InventoryRepository()
item_repo = ItemRepository()


@inventory_bp.route('/<user_id>')
def view_inventory(user_id):
    inventory = inventory_repo.get_user_inventory(user_id)
    items = item_repo.get_store_items()
    
    inventory_items = []
    for inv in inventory:
        item = next((i for i in items if i.ItemID == inv.ItemID), None)
        if item:
            inventory_items.append({
                'inventory_id': inv.InventoryID,
                'item': item,
                'status': inv.Status
            })
    
    return render_template('inventory.html', inventory=inventory_items, user_id=user_id)

@inventory_bp.route('/<user_id>/add/<inventory_id>', methods=['POST'])
def add_item(user_id, inventory_id):
    inventory = inventory_repo.get_user_inventory(user_id)
    inv_item = next((i for i in inventory if i.InventoryID == inventory_id), None)
    
    if inv_item:
        if inv_item.Status == 'unequipped':
            inventory_repo.update_item_status(inventory_id, 'equipped')
            flash('Item equipped!')
        else:
            flash('Item is already equipped')
    else:
        flash('Item not found in inventory')
    
    return redirect(url_for('inventory.view_inventory', user_id=user_id))

@inventory_bp.route('/<user_id>/remove/<inventory_id>', methods=['POST'])
def remove_item(user_id, inventory_id):
    inventory = inventory_repo.get_user_inventory(user_id)
    inv_item = next((i for i in inventory if i.InventoryID == inventory_id), None)
    
    if inv_item:
        if inv_item.Status == 'equipped':
            inventory_repo.update_item_status(inventory_id, 'unequipped')
            flash('Item unequipped!')
        else:
            flash('Item is already unequipped')
    else:
        flash('Item not found in inventory')
    
    return redirect(url_for('inventory.view_inventory', user_id=user_id))