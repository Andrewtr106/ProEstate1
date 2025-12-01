#!/usr/bin/env python3
"""
Test script to verify database integrity after adding new properties
"""

from flask import Flask
from models import db, Property
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def test_database():
    """Test database for property count and integrity"""
    app = create_app()

    with app.app_context():
        # Get total count
        total_properties = Property.query.count()
        print(f"Total properties in database: {total_properties}")

        # Check for duplicates by title
        titles = [prop.title for prop in Property.query.all()]
        duplicates = [title for title in titles if titles.count(title) > 1]
        if duplicates:
            print(f"Duplicate titles found: {set(duplicates)}")
        else:
            print("No duplicate titles found.")

        # Sample some properties to verify details
        sample_properties = Property.query.limit(5).all()
        print("\nSample properties:")
        for prop in sample_properties:
            print(f"- {prop.title}: {prop.location}, {prop.property_type}, EGP {prop.price:,}")

        # Check new properties specifically
        new_titles = [
            'Luxury Apartment in Heliopolis',
            'Seaside Villa in Alexandria',
            'Commercial Plaza in Tanta',
            'Beachfront Land in Hurghada',
            'Modern Townhouse in Obour City',
            'Riverside Apartment in Mansoura',
            'Historic Villa in Port Said',
            'Industrial Warehouse in Suez',
            'Desert Resort Land in Marsa Alam',
            'Canal View Apartment in Ismailia'
        ]

        found_new = 0
        for title in new_titles:
            prop = Property.query.filter_by(title=title).first()
            if prop:
                found_new += 1
                print(f"✓ Found new property: {title}")
            else:
                print(f"✗ Missing new property: {title}")

        print(f"\nFound {found_new}/10 new properties")

        # Check data integrity
        invalid_properties = Property.query.filter(
            (Property.price <= 0) |
            (Property.area <= 0) |
            (Property.bedrooms < 0) |
            (Property.bathrooms < 0)
        ).all()

        if invalid_properties:
            print(f"Found {len(invalid_properties)} properties with invalid data:")
            for prop in invalid_properties:
                print(f"- {prop.title}: price={prop.price}, area={prop.area}, beds={prop.bedrooms}, baths={prop.bathrooms}")
        else:
            print("All properties have valid data.")

if __name__ == '__main__':
    test_database()
