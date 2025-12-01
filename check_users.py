from flask import Flask
from models import db, User
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def check_users():
    app = create_app()
    with app.app_context():
        users = User.query.all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Name: {user.first_name} {user.last_name}")
            print(f"Password hash: {user.password_hash}")
            print("---")

if __name__ == '__main__':
    check_users()
