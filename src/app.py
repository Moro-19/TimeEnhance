from flask import Flask
from Controllers.User_controller import user_bp
from Controllers.Task_controller import task_bp
from Controllers.StoreItem_controller import store_bp
from Controllers.Inventory_controller import inventory_bp
from Controllers.Reward_controller import reward_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

app.register_blueprint(user_bp)
app.register_blueprint(task_bp)
app.register_blueprint(store_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(reward_bp)

@app.route('/')
def home():
    return "Welcome to Time Enhance!"

if __name__ == '__main__':
    app.run(debug=True)