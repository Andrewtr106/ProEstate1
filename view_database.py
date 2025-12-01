#!/usr/bin/env python3
"""
Script to view all data in the ProEstate database
"""

from flask import Flask
from models import db, User, Property, Favorite, ContactMessage
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def view_all_data():
    """Display all data from all tables in the database"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("📊 PROESTATE DATABASE CONTENTS")
        print("=" * 60)

        # Users
        print("\n👥 USERS:")
        print("-" * 40)
        users = User.query.all()
        if users:
            for user in users:
                print(f"ID: {user.id}")
                print(f"Email: {user.email}")
                print(f"Name: {user.first_name} {user.last_name}")
                print(f"Phone: {user.phone}")
                print(f"Admin: {user.is_admin}")
                print(f"Active: {user.is_active}")
                print(f"Created: {user.created_at}")
                print("-" * 20)
        else:
            print("No users found.")

        # Properties
        print("\n🏠 PROPERTIES:")
        print("-" * 40)
        properties = Property.query.all()
        if properties:
            for prop in properties:
                print(f"ID: {prop.id}")
                print(f"Title: {prop.title}")
                print(f"Type: {prop.property_type}")
                print(f"Location: {prop.location}")
                print(f"Price: EGP {prop.price:,.0f}")
                print(f"Area: {prop.area} sqm")
                print(f"Bedrooms: {prop.bedrooms}")
                print(f"Bathrooms: {prop.bathrooms}")
                print(f"Status: {prop.status}")
                print(f"Owner ID: {prop.user_id}")
                print(f"Created: {prop.created_at}")
                print("-" * 20)
        else:
            print("No properties found.")

        # Favorites
        print("\n❤️ FAVORITES:")
        print("-" * 40)
        favorites = Favorite.query.all()
        if favorites:
            for fav in favorites:
                print(f"ID: {fav.id}")
                print(f"User ID: {fav.user_id}")
                print(f"Property ID: {fav.property_id}")
                print(f"Created: {fav.created_at}")
                print("-" * 20)
        else:
            print("No favorites found.")

        # Contact Messages
        print("\n💬 CONTACT MESSAGES:")
        print("-" * 40)
        messages = ContactMessage.query.all()
        if messages:
            for msg in messages:
                print(f"ID: {msg.id}")
                print(f"Name: {msg.name}")
                print(f"Email: {msg.email}")
                print(f"Phone: {msg.phone}")
                print(f"Subject: {msg.subject}")
                print(f"Message: {msg.message[:100]}{'...' if len(msg.message) > 100 else ''}")
                print(f"Property ID: {msg.property_id}")
                print(f"Read: {msg.is_read}")
                print(f"Created: {msg.created_at}")
                print("-" * 20)
        else:
            print("No contact messages found.")

        # Summary
        print("\n📈 SUMMARY:")
        print("-" * 40)
        print(f"Total Users: {User.query.count()}")
        print(f"Total Properties: {Property.query.count()}")
        print(f"Total Favorites: {Favorite.query.count()}")
        print(f"Total Contact Messages: {ContactMessage.query.count()}")
        print("=" * 60)

if __name__ == '__main__':
    view_all_data()
