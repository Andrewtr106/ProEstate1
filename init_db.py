from models import Property, ContactMessage, User
from db_utils import DatabaseConnection
from datetime import datetime

def create_tables():
    """Create database tables using raw SQL"""
    db_conn = DatabaseConnection()

    # Drop tables if they exist (in reverse order due to foreign keys)
    drop_queries = [
        "IF OBJECT_ID('chat_history', 'U') IS NOT NULL DROP TABLE chat_history;",
        "IF OBJECT_ID('contact_messages', 'U') IS NOT NULL DROP TABLE contact_messages;",
        "IF OBJECT_ID('favorites', 'U') IS NOT NULL DROP TABLE favorites;",
        "IF OBJECT_ID('properties', 'U') IS NOT NULL DROP TABLE properties;",
        "IF OBJECT_ID('users', 'U') IS NOT NULL DROP TABLE users;"
    ]

    # Create tables
    create_queries = [
        """
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            email NVARCHAR(120) UNIQUE NOT NULL,
            password_hash NVARCHAR(256),
            first_name NVARCHAR(100),
            last_name NVARCHAR(100),
            phone NVARCHAR(20),
            created_at DATETIME2 DEFAULT GETDATE(),
            is_active BIT DEFAULT 1,
            is_admin BIT DEFAULT 0
        );
        """,
        """
        CREATE TABLE properties (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(200) NOT NULL,
            description NVARCHAR(MAX) NOT NULL,
            price FLOAT NOT NULL,
            property_type NVARCHAR(50) NOT NULL,
            location NVARCHAR(200) NOT NULL,
            area FLOAT NOT NULL,
            bedrooms INT DEFAULT 0,
            bathrooms INT DEFAULT 0,
            down_payment FLOAT,
            monthly_installment FLOAT,
            installment_years INT,
            image NVARCHAR(300),
            created_at DATETIME2 DEFAULT GETDATE(),
            updated_at DATETIME2 DEFAULT GETDATE(),
            status NVARCHAR(20) DEFAULT 'available',
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """,
        """
        CREATE TABLE favorites (
            id INT IDENTITY(1,1) PRIMARY KEY,
            user_id INT NOT NULL,
            property_id INT NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (property_id) REFERENCES properties(id)
        );
        """,
        """
        CREATE TABLE contact_messages (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            email NVARCHAR(100) NOT NULL,
            phone NVARCHAR(20),
            subject NVARCHAR(200),
            message NVARCHAR(MAX) NOT NULL,
            property_id INT,
            created_at DATETIME2 DEFAULT GETDATE(),
            is_read BIT DEFAULT 0,
            FOREIGN KEY (property_id) REFERENCES properties(id)
        );
        """,
        """
        CREATE TABLE chat_history (
            id INT IDENTITY(1,1) PRIMARY KEY,
            user_id INT,
            timestamp DATETIME2 DEFAULT GETDATE(),
            role NVARCHAR(10) NOT NULL,  -- 'user' or 'assistant'
            message NVARCHAR(MAX) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    ]

    try:
        # Drop existing tables
        for query in drop_queries:
            db_conn.execute(query)

        # Create new tables
        for query in create_queries:
            db_conn.execute(query)

        db_conn.commit()
        print("✅ Database tables created successfully!")
        return True

    except Exception as e:
        db_conn.rollback()
        print(f"❌ Error creating tables: {str(e)}")
        return False
    finally:
        db_conn.close()

def init_database():
    try:
        # Create tables
        if not create_tables():
            return False

        # Create sample user
        user = User.create(
            email="admin@proestate.com",
            first_name="Admin",
            last_name="User",
            phone="+201002532510",
            password="admin123",
            is_admin=True
        )
        print("✅ Sample user created successfully!")

        # Sample properties data
        sample_properties_data = [
            # Original 5 properties
            {
                "title": "Luxury Apartment in New Cairo",
                "description": "Beautiful 3-bedroom apartment in prime New Cairo location. Features modern finishing, panoramic views, and premium amenities including swimming pool, gym, and 24/7 security. Located in a gated community with green spaces and children's playground.",
                "price": 4500000,
                "property_type": "Apartment",
                "location": "New Cairo, Cairo",
                "area": 180,
                "bedrooms": 3,
                "bathrooms": 2,
                "down_payment": 900000,
                "monthly_installment": 35000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Modern Villa in Sheikh Zayed",
                "description": "Spacious 4-bedroom villa with private garden and swimming pool. Perfect for families seeking luxury living in Sheikh Zayed. Features include marble flooring, modern kitchen, maid's room, and private parking for 3 cars.",
                "price": 8500000,
                "property_type": "Villa",
                "location": "Sheikh Zayed, Giza",
                "area": 320,
                "bedrooms": 4,
                "bathrooms": 3,
                "down_payment": 1700000,
                "monthly_installment": 68000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1613977257363-707ba9348227?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Penthouse with Nile View",
                "description": "Exclusive penthouse with breathtaking Nile River views. Features 3 bedrooms, large living area, and expansive terrace. Premium finishes throughout with high-end appliances and smart home system.",
                "price": 12000000,
                "property_type": "Penthouse",
                "location": "Zamalek, Cairo",
                "area": 280,
                "bedrooms": 3,
                "bathrooms": 3,
                "down_payment": 2400000,
                "monthly_installment": 95000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Townhouse in Rehab City",
                "description": "Modern townhouse in family-friendly Rehab City. 3 bedrooms, 2.5 bathrooms, private garden, and shared community facilities including pool, gym, and sports courts.",
                "price": 3800000,
                "property_type": "Townhouse",
                "location": "Rehab City, Cairo",
                "area": 200,
                "bedrooms": 3,
                "bathrooms": 2,
                "down_payment": 760000,
                "monthly_installment": 30000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Commercial Space in Downtown",
                "description": "Prime commercial space in downtown Cairo ideal for retail or office use. High foot traffic area with excellent visibility. Ready for immediate occupancy with basic finishing.",
                "price": 6500000,
                "property_type": "Commercial",
                "location": "Downtown Cairo",
                "area": 150,
                "bedrooms": 0,
                "bathrooms": 2,
                "down_payment": 1300000,
                "monthly_installment": 52000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },

            # 5 NEW PROPERTIES
            {
                "title": "Beachfront Apartment in North Coast",
                "description": "Stunning beachfront apartment in North Coast with direct sea access. 2 bedrooms, modern kitchen, and large balcony with panoramic sea views. Perfect for vacation or investment.",
                "price": 3200000,
                "property_type": "Apartment",
                "location": "North Coast",
                "area": 120,
                "bedrooms": 2,
                "bathrooms": 2,
                "down_payment": 640000,
                "monthly_installment": 25000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Family Villa in Madinaty",
                "description": "Elegant 5-bedroom villa in Madinaty compound. Spacious living areas, modern kitchen, private garden, and access to community amenities including pools, parks, and clubhouse.",
                "price": 7500000,
                "property_type": "Villa",
                "location": "Madinaty, Cairo",
                "area": 350,
                "bedrooms": 5,
                "bathrooms": 4,
                "down_payment": 1500000,
                "monthly_installment": 60000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Investment Land in 6th of October",
                "description": "Prime investment land in rapidly developing 6th of October City. Ideal for residential or commercial development. Clear title and all utilities available at site.",
                "price": 2500000,
                "property_type": "Land",
                "location": "6th of October City",
                "area": 500,
                "bedrooms": 0,
                "bathrooms": 0,
                "down_payment": 500000,
                "monthly_installment": 20000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Luxury Duplex in Katameya Heights",
                "description": "Stunning duplex apartment in Katameya Heights with private elevator. 4 bedrooms, study room, and large terrace with golf course views. Premium finishes throughout.",
                "price": 6800000,
                "property_type": "Apartment",
                "location": "Katameya Heights, Cairo",
                "area": 240,
                "bedrooms": 4,
                "bathrooms": 3,
                "down_payment": 1360000,
                "monthly_installment": 54000,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Studio Apartment in Nasr City",
                "description": "Compact studio apartment perfect for singles or young couples. Modern finishing, built-in kitchen, and balcony. Great investment opportunity with high rental yield.",
                "price": 850000,
                "property_type": "Apartment",
                "location": "Nasr City, Cairo",
                "area": 45,
                "bedrooms": 1,
                "bathrooms": 1,
                "down_payment": 170000,
                "monthly_installment": 6800,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Garden Apartment in Maadi",
                "description": "Charming ground floor apartment with private garden in quiet Maadi street. 2 bedrooms, renovated kitchen, and spacious living area. Perfect for small families.",
                "price": 2200000,
                "property_type": "Apartment",
                "location": "Maadi, Cairo",
                "area": 110,
                "bedrooms": 2,
                "bathrooms": 2,
                "down_payment": 440000,
                "monthly_installment": 17500,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Modern Office Space in Heliopolis",
                "description": "Professional office space in Heliopolis business district. Ready for immediate occupancy with partitioning, AC, and high-speed internet infrastructure.",
                "price": 4200000,
                "property_type": "Commercial",
                "location": "Heliopolis, Cairo",
                "area": 180,
                "bedrooms": 0,
                "bathrooms": 2,
                "down_payment": 840000,
                "monthly_installment": 33500,
                "installment_years": 10,
                "image": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            }
        ]

        # Create properties
        created_properties = []
        for prop_data in sample_properties_data:
            prop = Property.create(**prop_data)
            created_properties.append(prop)

        print(f"✅ {len(created_properties)} sample properties created successfully!")

        # Add sample contact message
        sample_message = ContactMessage.create(
            name="Ahmed Mohamed",
            email="ahmed@example.com",
            phone="+201002532510",
            subject="Inquiry about Villa in Sheikh Zayed",
            message="I'm interested in the villa in Sheikh Zayed. Can you please provide more details about the payment plan and schedule a viewing?",
            property_id=2
        )
        print("✅ Sample contact message created successfully!")

        print(f"✅ Sample data added successfully!")
        print(f"✅ Added {len(created_properties)} properties, 1 user, and 1 contact message")
        print("👤 Default admin login: admin@proestate.com / admin123")
        return True

    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False

if __name__ == '__main__':
    print("🔄 Initializing ProEstate Database...")
    success = init_database()
    if success:
        print("\n🎉 Database initialization completed!")
        print("📊 You can now run the application using: python run.py")
    else:
        print("\n❌ Database initialization failed!")
