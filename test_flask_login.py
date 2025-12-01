#!/usr/bin/env python3
"""
Test script to verify Flask-Login authentication system
"""
import sys
import os
import uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from flask_login import current_user, login_user, logout_user

def test_flask_login():
    """Test Flask-Login functionality"""
    print("Testing Flask-Login authentication system...")

    with app.app_context():
        # Create all tables
        db.create_all()

        # Test 1: Create a test user
        print("\n1. Creating test user...")
        unique_id = str(uuid.uuid4())[:8]
        test_email = f"test_{unique_id}@example.com"
        test_user = User(
            email=test_email,
            first_name="Test",
            last_name="User",
            phone="1234567890"
        )
        test_user.set_password("password123")
        db.session.add(test_user)
        db.session.commit()
        print("✓ Test user created successfully")

        # Test 2: Test password verification
        print("\n2. Testing password verification...")
        assert test_user.check_password("password123"), "Password check failed"
        assert not test_user.check_password("wrongpassword"), "Password check should fail"
        print("✓ Password verification working correctly")

        # Test 3: Test UserMixin methods
        print("\n3. Testing UserMixin methods...")
        assert test_user.is_authenticated, "User should be authenticated"
        assert not test_user.is_anonymous, "User should not be anonymous"
        assert test_user.get_id() == str(test_user.id), "get_id() should return user ID"
        print("✓ UserMixin methods working correctly")

        # Test 4: Test admin user creation
        print("\n4. Creating admin user...")
        admin_unique_id = str(uuid.uuid4())[:8]
        admin_email = f"admin_{admin_unique_id}@example.com"
        admin_user = User(
            email=admin_email,
            first_name="Admin",
            last_name="User",
            phone="0987654321",
            is_admin=True
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        db.session.commit()
        assert admin_user.is_admin, "Admin user should have admin privileges"
        print("✓ Admin user created successfully")

        # Test 5: Test login_user functionality
        print("\n5. Testing login_user functionality...")
        with app.test_request_context():
            # Initially no user should be logged in
            assert not current_user.is_authenticated, "No user should be initially authenticated"

            # Login the test user
            login_user(test_user)
            assert current_user.is_authenticated, "User should be authenticated after login"
            assert current_user.id == test_user.id, "Current user should match logged in user"
            assert current_user.email == test_user.email, "Current user email should match"

            # Logout
            logout_user()
            assert not current_user.is_authenticated, "User should not be authenticated after logout"

        print("✓ login_user functionality working correctly")

        print("\n✅ All Flask-Login tests passed!")

        # Clean up
        db.session.delete(test_user)
        db.session.delete(admin_user)
        db.session.commit()

if __name__ == "__main__":
    test_flask_login()
