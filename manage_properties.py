#!/usr/bin/env python3
"""
ProEstate Property Management Script
Handles property deletion and addition with sample data
"""

import os
from flask import Flask
from models import db, Property
from config import Config
from add_more_properties import add_more_properties

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def delete_all_properties():
    """Delete all existing properties"""
    try:
        deleted_count = Property.query.delete()
        db.session.commit()
        print(f"Deleted {deleted_count} existing properties")
        return True
    except Exception as e:
        print(f"Error deleting properties: {e}")
        db.session.rollback()
        return False

def add_sample_properties():
    """Add sample properties with good photos and details"""
    properties_data = [
        {
            'title': 'Luxury Villa in New Cairo',
            'description': 'Stunning 4-bedroom villa in the prestigious New Cairo district. Features modern architecture, private garden, swimming pool, and premium finishes. Perfect for families seeking luxury living with easy access to schools, shopping centers, and business districts.',
            'price': 8500000,
            'property_type': 'Villa',
            'location': 'New Cairo, Cairo',
            'area': 350.0,
            'bedrooms': 4,
            'bathrooms': 3,
            'down_payment': 850000,
            'monthly_installment': 70833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Modern Apartment in Zamalek',
            'description': 'Elegant 3-bedroom apartment in the heart of Zamalek. Overlooking the Nile River with panoramic views. Features high-end finishes, modern kitchen, and spacious living areas. Walking distance to restaurants, cafes, and cultural attractions.',
            'price': 4200000,
            'property_type': 'Apartment',
            'location': 'Zamalek, Cairo',
            'area': 180.0,
            'bedrooms': 3,
            'bathrooms': 2,
            'down_payment': 420000,
            'monthly_installment': 35000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Townhouse in 6th of October',
            'description': 'Beautiful 3-story townhouse in a gated community. Features 4 bedrooms, private garage, and landscaped garden. Located in a family-friendly neighborhood with excellent schools and shopping facilities nearby.',
            'price': 3200000,
            'property_type': 'Townhouse',
            'location': '6th of October City, Giza',
            'area': 220.0,
            'bedrooms': 4,
            'bathrooms': 3,
            'down_payment': 320000,
            'monthly_installment': 26667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Penthouse in Downtown Cairo',
            'description': 'Exclusive penthouse with stunning city views. 3 bedrooms, 3 bathrooms, and a large terrace perfect for entertaining. Modern design with premium materials and smart home features. Located in the vibrant downtown area.',
            'price': 6500000,
            'property_type': 'Apartment',
            'location': 'Downtown Cairo',
            'area': 250.0,
            'bedrooms': 3,
            'bathrooms': 3,
            'down_payment': 650000,
            'monthly_installment': 54167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Commercial Space in Heliopolis',
            'description': 'Prime commercial space in Heliopolis business district. Perfect for retail, office, or medical practice. High foot traffic location with excellent visibility and parking availability.',
            'price': 5500000,
            'property_type': 'Commercial',
            'location': 'Heliopolis, Cairo',
            'area': 150.0,
            'bedrooms': 0,
            'bathrooms': 2,
            'down_payment': 550000,
            'monthly_installment': 45833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Land Plot in North Coast',
            'description': 'Prime land plot in the prestigious North Coast area. 1000 sqm plot perfect for villa construction. Located in a gated community with beach access and all utilities available.',
            'price': 2800000,
            'property_type': 'Land',
            'location': 'North Coast, Egypt',
            'area': 1000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 280000,
            'monthly_installment': 23333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Spacious Villa in Maadi',
            'description': 'Impressive 5-bedroom villa in the upscale Maadi district. Features a large garden, swimming pool, and modern amenities. Perfect for large families with excellent access to international schools and diplomatic compounds.',
            'price': 9200000,
            'property_type': 'Villa',
            'location': 'Maadi, Cairo',
            'area': 400.0,
            'bedrooms': 5,
            'bathrooms': 4,
            'down_payment': 920000,
            'monthly_installment': 76667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Cozy Apartment in Garden City',
            'description': 'Charming 2-bedroom apartment in the historic Garden City area. Features original architectural details, high ceilings, and modern updates. Walking distance to the Nile Corniche and cultural landmarks.',
            'price': 3800000,
            'property_type': 'Apartment',
            'location': 'Garden City, Cairo',
            'area': 140.0,
            'bedrooms': 2,
            'bathrooms': 2,
            'down_payment': 380000,
            'monthly_installment': 31667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Modern Townhouse in Sheikh Zayed',
            'description': 'Contemporary 3-story townhouse in Sheikh Zayed City. Features smart home technology, private elevator, and rooftop terrace. Located in a secure compound with 24/7 security and recreational facilities.',
            'price': 4500000,
            'property_type': 'Townhouse',
            'location': 'Sheikh Zayed City, Giza',
            'area': 280.0,
            'bedrooms': 4,
            'bathrooms': 4,
            'down_payment': 450000,
            'monthly_installment': 37500,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Luxury Penthouse in Nasr City',
            'description': 'Ultra-modern penthouse with floor-to-ceiling windows and breathtaking city skyline views. 4 bedrooms, 4 bathrooms, and a private rooftop pool. Premium finishes and state-of-the-art appliances throughout.',
            'price': 7800000,
            'property_type': 'Apartment',
            'location': 'Nasr City, Cairo',
            'area': 320.0,
            'bedrooms': 4,
            'bathrooms': 4,
            'down_payment': 780000,
            'monthly_installment': 65000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Retail Space in Mohandessin',
            'description': 'High-visibility retail space in the bustling Mohandessin district. Perfect for boutique shops, cafes, or professional offices. Excellent foot traffic and prime location near major transportation hubs.',
            'price': 6200000,
            'property_type': 'Commercial',
            'location': 'Mohandessin, Giza',
            'area': 180.0,
            'bedrooms': 0,
            'bathrooms': 3,
            'down_payment': 620000,
            'monthly_installment': 51667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Beachfront Land in Alexandria',
            'description': 'Rare beachfront land plot in the Mediterranean city of Alexandria. 800 sqm plot with direct sea access. Perfect for luxury villa development with stunning coastal views and year-round mild climate.',
            'price': 5200000,
            'property_type': 'Land',
            'location': 'Alexandria, Egypt',
            'area': 800.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 520000,
            'monthly_installment': 43333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Elegant Villa in Rehab City',
            'description': 'Sophisticated 4-bedroom villa in the exclusive Rehab City compound. Features Mediterranean architecture, landscaped gardens, and resort-style amenities. Access to golf courses, schools, and shopping within the compound.',
            'price': 6800000,
            'property_type': 'Villa',
            'location': 'Rehab City, New Cairo',
            'area': 320.0,
            'bedrooms': 4,
            'bathrooms': 3,
            'down_payment': 680000,
            'monthly_installment': 56667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Studio Apartment in Dokki',
            'description': 'Stylish studio apartment in the vibrant Dokki neighborhood. Perfect for young professionals or investors. Modern furnishings, built-in appliances, and excellent location near universities and business centers.',
            'price': 1800000,
            'property_type': 'Apartment',
            'location': 'Dokki, Giza',
            'area': 85.0,
            'bedrooms': 1,
            'bathrooms': 1,
            'down_payment': 180000,
            'monthly_installment': 15000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Duplex Townhouse in Beverly Hills',
            'description': 'Luxurious duplex townhouse in the prestigious Beverly Hills compound. Features 5 bedrooms, private elevator, and expansive living spaces. Resort amenities include pools, gyms, and kids play areas.',
            'price': 5800000,
            'property_type': 'Townhouse',
            'location': 'Beverly Hills, Sheikh Zayed',
            'area': 350.0,
            'bedrooms': 5,
            'bathrooms': 5,
            'down_payment': 580000,
            'monthly_installment': 48333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Office Space in Smart Village',
            'description': 'Modern office space in the technology hub of Smart Village. Fully equipped with high-speed internet, meeting rooms, and parking. Perfect for tech startups, consulting firms, or corporate offices.',
            'price': 4800000,
            'property_type': 'Commercial',
            'location': 'Smart Village, Giza',
            'area': 200.0,
            'bedrooms': 0,
            'bathrooms': 4,
            'down_payment': 480000,
            'monthly_installment': 40000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Agricultural Land in Fayoum',
            'description': 'Fertile agricultural land in the Fayoum oasis. 2000 sqm plot suitable for various crops. Access to irrigation systems and located in a productive farming region with excellent market access.',
            'price': 1200000,
            'property_type': 'Land',
            'location': 'Fayoum, Egypt',
            'area': 2000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 120000,
            'monthly_installment': 10000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Charming Cottage in Luxor',
            'description': 'Historic cottage-style home in the ancient city of Luxor. Features traditional architecture with modern amenities. Perfect for those seeking a unique living experience near world-famous temples and monuments.',
            'price': 2200000,
            'property_type': 'Villa',
            'location': 'Luxor, Egypt',
            'area': 180.0,
            'bedrooms': 3,
            'bathrooms': 2,
            'down_payment': 220000,
            'monthly_installment': 18333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'High-Rise Apartment in Sharm El Sheikh',
            'description': 'Stunning beachfront apartment in Sharm El Sheikh. Features floor-to-ceiling windows with Red Sea views, infinity pool access, and resort amenities. Ideal for vacation homes or investment properties.',
            'price': 3500000,
            'property_type': 'Apartment',
            'location': 'Sharm El Sheikh, Egypt',
            'area': 120.0,
            'bedrooms': 2,
            'bathrooms': 2,
            'down_payment': 350000,
            'monthly_installment': 29167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Warehouse Space in Industrial Zone',
            'description': 'Large warehouse facility in Cairo\'s industrial zone. Perfect for manufacturing, storage, or distribution operations. Features high ceilings, loading docks, and excellent transportation access.',
            'price': 7500000,
            'property_type': 'Commercial',
            'location': 'Industrial Zone, Cairo',
            'area': 500.0,
            'bedrooms': 0,
            'bathrooms': 2,
            'down_payment': 750000,
            'monthly_installment': 62500,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Desert Land in Siwa Oasis',
            'description': 'Unique desert land plot in the mystical Siwa Oasis. 1500 sqm plot surrounded by natural beauty and ancient history. Perfect for eco-tourism development or private retreat.',
            'price': 800000,
            'property_type': 'Land',
            'location': 'Siwa Oasis, Egypt',
            'area': 1500.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 80000,
            'monthly_installment': 6667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Boutique Hotel in Aswan',
            'description': 'Converted historic building into a boutique hotel in Aswan. Features Nile River views, traditional Nubian architecture, and authentic local charm. Includes 8 guest rooms and restaurant space.',
            'price': 9500000,
            'property_type': 'Commercial',
            'location': 'Aswan, Egypt',
            'area': 400.0,
            'bedrooms': 8,
            'bathrooms': 10,
            'down_payment': 950000,
            'monthly_installment': 79167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Mountain View Villa in Sinai',
            'description': 'Spectacular villa with panoramic mountain views in South Sinai. Features traditional Bedouin architecture with modern comforts. Perfect for nature lovers seeking tranquility and adventure.',
            'price': 4200000,
            'property_type': 'Villa',
            'location': 'South Sinai, Egypt',
            'area': 250.0,
            'bedrooms': 3,
            'bathrooms': 3,
            'down_payment': 420000,
            'monthly_installment': 35000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Luxury Apartment in Heliopolis',
            'description': 'Modern 3-bedroom apartment in the upscale Heliopolis district. Features smart home technology, private balcony with city views, and premium finishes. Located near international schools and shopping centers.',
            'price': 5500000,
            'property_type': 'Apartment',
            'location': 'Heliopolis, Cairo',
            'area': 160.0,
            'bedrooms': 3,
            'bathrooms': 2,
            'down_payment': 550000,
            'monthly_installment': 45833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Seaside Villa in Alexandria',
            'description': 'Elegant 4-bedroom villa overlooking the Mediterranean Sea in Alexandria. Features a private beach access, infinity pool, and traditional Alexandrian architecture blended with modern amenities.',
            'price': 7200000,
            'property_type': 'Villa',
            'location': 'Alexandria, Egypt',
            'area': 350.0,
            'bedrooms': 4,
            'bathrooms': 4,
            'down_payment': 720000,
            'monthly_installment': 60000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Commercial Plaza in Tanta',
            'description': 'Prime commercial space in Tanta\'s bustling business district. Multi-level retail and office complex with excellent visibility and high foot traffic. Perfect for retail chains or professional services.',
            'price': 8500000,
            'property_type': 'Commercial',
            'location': 'Tanta, Gharbia',
            'area': 300.0,
            'bedrooms': 0,
            'bathrooms': 6,
            'down_payment': 850000,
            'monthly_installment': 70833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Beachfront Land in Hurghada',
            'description': 'Premium beachfront land plot in Hurghada\'s luxury resort area. 1200 sqm plot with direct Red Sea access. Ideal for developing a high-end resort villa or boutique hotel.',
            'price': 6800000,
            'property_type': 'Land',
            'location': 'Hurghada, Red Sea',
            'area': 1200.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 680000,
            'monthly_installment': 56667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Modern Townhouse in Obour City',
            'description': 'Contemporary 4-story townhouse in the developing Obour City area. Features rooftop terrace, private garage, and smart home features. Located in a family-friendly community with easy access to Cairo.',
            'price': 3800000,
            'property_type': 'Townhouse',
            'location': 'Obour City, Cairo',
            'area': 240.0,
            'bedrooms': 4,
            'bathrooms': 3,
            'down_payment': 380000,
            'monthly_installment': 31667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Riverside Apartment in Mansoura',
            'description': 'Charming 2-bedroom apartment with Nile River views in Mansoura. Features traditional architecture with modern updates, high ceilings, and original details. Walking distance to universities and cultural sites.',
            'price': 2800000,
            'property_type': 'Apartment',
            'location': 'Mansoura, Dakahlia',
            'area': 120.0,
            'bedrooms': 2,
            'bathrooms': 2,
            'down_payment': 280000,
            'monthly_installment': 23333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Historic Villa in Port Said',
            'description': 'Restored historic villa in Port Said\'s colonial quarter. Features original architectural details, large gardens, and modern amenities. Perfect for those seeking character and charm near the Suez Canal.',
            'price': 4500000,
            'property_type': 'Villa',
            'location': 'Port Said, Egypt',
            'area': 280.0,
            'bedrooms': 3,
            'bathrooms': 3,
            'down_payment': 450000,
            'monthly_installment': 37500,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Industrial Warehouse in Suez',
            'description': 'Large industrial warehouse in Suez\'s free trade zone. Features high ceilings, multiple loading docks, and excellent transportation access. Perfect for manufacturing, logistics, or storage operations.',
            'price': 9200000,
            'property_type': 'Commercial',
            'location': 'Suez, Egypt',
            'area': 800.0,
            'bedrooms': 0,
            'bathrooms': 4,
            'down_payment': 920000,
            'monthly_installment': 76667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Desert Resort Land in Marsa Alam',
            'description': 'Expansive desert land plot in Marsa Alam\'s luxury resort area. 2500 sqm plot perfect for developing an eco-resort or private retreat. Surrounded by natural beauty and marine protected areas.',
            'price': 3500000,
            'property_type': 'Land',
            'location': 'Marsa Alam, Red Sea',
            'area': 2500.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 350000,
            'monthly_installment': 29167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Canal View Apartment in Ismailia',
            'description': 'Modern 3-bedroom apartment with Suez Canal views in Ismailia. Features contemporary design, private terrace, and resort-style amenities. Located in a secure compound near military and diplomatic areas.',
            'price': 3200000,
            'property_type': 'Apartment',
            'location': 'Ismailia, Egypt',
            'area': 140.0,
            'bedrooms': 3,
            'bathrooms': 2,
            'down_payment': 320000,
            'monthly_installment': 26667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        }
    ]

    added_count = 0
    for prop_data in properties_data:
        try:
            # Create property
            property = Property(
                title=prop_data['title'],
                description=prop_data['description'],
                price=prop_data['price'],
                property_type=prop_data['property_type'],
                location=prop_data['location'],
                area=prop_data['area'],
                bedrooms=prop_data['bedrooms'],
                bathrooms=prop_data['bathrooms'],
                down_payment=prop_data['down_payment'],
                monthly_installment=prop_data['monthly_installment'],
                installment_years=prop_data['installment_years'],
                image=prop_data['image'],
                status='available'
            )

            db.session.add(property)
            db.session.commit()
            added_count += 1
            print(f"Added property: {prop_data['title']}")

        except Exception as e:
            print(f"Error adding property {prop_data['title']}: {e}")
            db.session.rollback()
            continue

    print(f"Successfully added {added_count} new properties")
    return added_count > 0

def add_additional_properties():
    """Add additional properties without deleting existing ones"""
    properties_data = [
        {
            'title': 'Luxury Apartment in Heliopolis',
            'description': 'Modern 3-bedroom apartment in the upscale Heliopolis district. Features smart home technology, private balcony with city views, and premium finishes. Located near international schools and shopping centers.',
            'price': 5500000,
            'property_type': 'Apartment',
            'location': 'Heliopolis, Cairo',
            'area': 160.0,
            'bedrooms': 3,
            'bathrooms': 2,
            'down_payment': 550000,
            'monthly_installment': 45833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Seaside Villa in Alexandria',
            'description': 'Elegant 4-bedroom villa overlooking the Mediterranean Sea in Alexandria. Features a private beach access, infinity pool, and traditional Alexandrian architecture blended with modern amenities.',
            'price': 7200000,
            'property_type': 'Villa',
            'location': 'Alexandria, Egypt',
            'area': 350.0,
            'bedrooms': 4,
            'bathrooms': 4,
            'down_payment': 720000,
            'monthly_installment': 60000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Commercial Plaza in Tanta',
            'description': 'Prime commercial space in Tanta\'s bustling business district. Multi-level retail and office complex with excellent visibility and high foot traffic. Perfect for retail chains or professional services.',
            'price': 8500000,
            'property_type': 'Commercial',
            'location': 'Tanta, Gharbia',
            'area': 300.0,
            'bedrooms': 0,
            'bathrooms': 6,
            'down_payment': 850000,
            'monthly_installment': 70833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Beachfront Land in Hurghada',
            'description': 'Premium beachfront land plot in Hurghada\'s luxury resort area. 1200 sqm plot with direct Red Sea access. Ideal for developing a high-end resort villa or boutique hotel.',
            'price': 6800000,
            'property_type': 'Land',
            'location': 'Hurghada, Red Sea',
            'area': 1200.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 680000,
            'monthly_installment': 56667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Modern Townhouse in Obour City',
            'description': 'Contemporary 4-story townhouse in the developing Obour City area. Features rooftop terrace, private garage, and smart home features. Located in a family-friendly community with easy access to Cairo.',
            'price': 3800000,
            'property_type': 'Townhouse',
            'location': 'Obour City, Cairo',
            'area': 240.0,
            'bedrooms': 4,
            'bathrooms': 3,
            'down_payment': 380000,
            'monthly_installment': 31667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Riverside Apartment in Mansoura',
            'description': 'Charming 2-bedroom apartment with Nile River views in Mansoura. Features traditional architecture with modern updates, high ceilings, and original details. Walking distance to universities and cultural sites.',
            'price': 2800000,
            'property_type': 'Apartment',
            'location': 'Mansoura, Dakahlia',
            'area': 120.0,
            'bedrooms': 2,
            'bathrooms': 2,
            'down_payment': 280000,
            'monthly_installment': 23333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Historic Villa in Port Said',
            'description': 'Restored historic villa in Port Said\'s colonial quarter. Features original architectural details, large gardens, and modern amenities. Perfect for those seeking character and charm near the Suez Canal.',
            'price': 4500000,
            'property_type': 'Villa',
            'location': 'Port Said, Egypt',
            'area': 280.0,
            'bedrooms': 3,
            'bathrooms': 3,
            'down_payment': 450000,
            'monthly_installment': 37500,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Industrial Warehouse in Suez',
            'description': 'Large industrial warehouse in Suez\'s free trade zone. Features high ceilings, multiple loading docks, and excellent transportation access. Perfect for manufacturing, logistics, or storage operations.',
            'price': 9200000,
            'property_type': 'Commercial',
            'location': 'Suez, Egypt',
            'area': 800.0,
            'bedrooms': 0,
            'bathrooms': 4,
            'down_payment': 920000,
            'monthly_installment': 76667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Desert Resort Land in Marsa Alam',
            'description': 'Expansive desert land plot in Marsa Alam\'s luxury resort area. 2500 sqm plot perfect for developing an eco-resort or private retreat. Surrounded by natural beauty and marine protected areas.',
            'price': 3500000,
            'property_type': 'Land',
            'location': 'Marsa Alam, Red Sea',
            'area': 2500.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 350000,
            'monthly_installment': 29167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Canal View Apartment in Ismailia',
            'description': 'Modern 3-bedroom apartment with Suez Canal views in Ismailia. Features contemporary design, private terrace, and resort-style amenities. Located in a secure compound near military and diplomatic areas.',
            'price': 3200000,
            'property_type': 'Apartment',
            'location': 'Ismailia, Egypt',
            'area': 140.0,
            'bedrooms': 3,
            'bathrooms': 2,
            'down_payment': 320000,
            'monthly_installment': 26667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        }
    ]

    added_count = 0
    for prop_data in properties_data:
        try:
            # Check if property already exists
            existing_property = Property.query.filter_by(title=prop_data['title']).first()
            if existing_property:
                print(f"Property '{prop_data['title']}' already exists, skipping...")
                continue

            # Create property
            property = Property(
                title=prop_data['title'],
                description=prop_data['description'],
                price=prop_data['price'],
                property_type=prop_data['property_type'],
                location=prop_data['location'],
                area=prop_data['area'],
                bedrooms=prop_data['bedrooms'],
                bathrooms=prop_data['bathrooms'],
                down_payment=prop_data['down_payment'],
                monthly_installment=prop_data['monthly_installment'],
                installment_years=prop_data['installment_years'],
                image=prop_data['image'],
                status='available'
            )

            db.session.add(property)
            db.session.commit()
            added_count += 1
            print(f"Added property: {prop_data['title']}")

        except Exception as e:
            print(f"Error adding property {prop_data['title']}: {e}")
            db.session.rollback()
            continue

    print(f"Successfully added {added_count} new properties")
    return added_count > 0

def main():
    """Main function to manage properties"""
    app = create_app()

    with app.app_context():
        print("✅ Adding 25 more properties to existing database...")
        add_success = add_more_properties()

        if add_success:
            print("🎉 Property addition completed successfully!")
            print("📸 All property images are set to default.jpg (you can replace with actual images)")
        else:
            print("❌ Failed to add new properties")

if __name__ == '__main__':
    main()
