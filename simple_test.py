from flask import Flask
from models import db, Property
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    total = Property.query.count()
    print(f"Total properties: {total}")

    if total > 0:
        first = Property.query.first()
        print(f"First property: {first.title}")

        # Check for new properties
        new_titles = ['Luxury Apartment in Heliopolis', 'Seaside Villa in Alexandria']
        for title in new_titles:
            prop = Property.query.filter_by(title=title).first()
            if prop:
                print(f"✓ Found: {title}")
            else:
                print(f"✗ Missing: {title}")

    print("Database test completed.")
