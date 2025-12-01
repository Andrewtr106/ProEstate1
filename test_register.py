from flask import Flask
from models import db, User
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def test_register():
    app = create_app()
    with app.app_context():
        # Check if test user exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if test_user:
            print("Test user already exists")
            print(f"Password hash: {test_user.password_hash}")
            # Test password check
            if test_user.check_password('testpassword'):
                print("Password check successful")
            else:
                print("Password check failed")
        else:
            # Create test user
            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
            print("Test user created successfully")
            print(f"Password hash: {user.password_hash}")

if __name__ == '__main__':
    test_register()
