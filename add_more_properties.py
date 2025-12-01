#!/usr/bin/env python3
"""
ProEstate Property Management Script
Handles adding 25 more properties to the database
"""

import os
from flask import Flask
from models import db, Property
from config import Config

def add_more_properties():
    """Add 25 more properties with all details"""
    properties_data = [
        {
            'title': 'Executive Office in Business Bay',
            'description': 'Premium executive office space in the heart of Business Bay. Features floor-to-ceiling windows, modern furnishings, and state-of-the-art conference facilities. Perfect for corporate headquarters or high-profile consulting firms.',
            'price': 12000000,
            'property_type': 'Commercial',
            'location': 'Business Bay, Dubai',
            'area': 400.0,
            'bedrooms': 0,
            'bathrooms': 8,
            'down_payment': 1200000,
            'monthly_installment': 100000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Lakefront Villa in 5th Settlement',
            'description': 'Stunning 5-bedroom villa with private lake access in the prestigious 5th Settlement. Features infinity pool, landscaped gardens, and panoramic water views. Includes private dock and boat house.',
            'price': 15000000,
            'property_type': 'Villa',
            'location': '5th Settlement, New Cairo',
            'area': 500.0,
            'bedrooms': 5,
            'bathrooms': 6,
            'down_payment': 1500000,
            'monthly_installment': 125000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Boutique Apartment in Zamalek',
            'description': 'Charming 1-bedroom apartment in the cultural heart of Zamalek. Features original Art Deco details, high ceilings, and Nile River views. Walking distance to galleries, theaters, and fine dining.',
            'price': 3500000,
            'property_type': 'Apartment',
            'location': 'Zamalek, Cairo',
            'area': 90.0,
            'bedrooms': 1,
            'bathrooms': 1,
            'down_payment': 350000,
            'monthly_installment': 29167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Agricultural Land in Beni Suef',
            'description': 'Fertile agricultural land in the productive Beni Suef governorate. 3000 sqm plot with irrigation access and fertile soil. Perfect for commercial farming operations or agricultural investment.',
            'price': 1800000,
            'property_type': 'Land',
            'location': 'Beni Suef, Egypt',
            'area': 3000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 180000,
            'monthly_installment': 15000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Luxury Penthouse in Katameya Heights',
            'description': 'Ultra-luxury penthouse in the exclusive Katameya Heights compound. Features 4 bedrooms, private elevator, rooftop garden, and 360-degree city views. Includes access to compound amenities and 24/7 security.',
            'price': 18000000,
            'property_type': 'Apartment',
            'location': 'Katameya Heights, New Cairo',
            'area': 450.0,
            'bedrooms': 4,
            'bathrooms': 5,
            'down_payment': 1800000,
            'monthly_installment': 150000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Traditional Townhouse in Islamic Cairo',
            'description': 'Authentic Islamic architecture townhouse in the historic Islamic Cairo district. Features traditional mashrabiya windows, courtyard garden, and restored architectural details. Walking distance to Citadel and Khan El Khalili.',
            'price': 5500000,
            'property_type': 'Townhouse',
            'location': 'Islamic Cairo',
            'area': 200.0,
            'bedrooms': 3,
            'bathrooms': 2,
            'down_payment': 550000,
            'monthly_installment': 45833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Medical Clinic Space in Mohandessin',
            'description': 'Prime medical clinic space in the healthcare hub of Mohandessin. Features reception area, examination rooms, and waiting lounge. Excellent location near major hospitals and medical centers.',
            'price': 4800000,
            'property_type': 'Commercial',
            'location': 'Mohandessin, Giza',
            'area': 120.0,
            'bedrooms': 0,
            'bathrooms': 3,
            'down_payment': 480000,
            'monthly_installment': 40000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Desert Land in White Desert',
            'description': 'Unique desert land plot in the spectacular White Desert National Park. 5000 sqm plot featuring dramatic chalk rock formations and surreal landscapes. Perfect for eco-lodge development or astronomical tourism.',
            'price': 2500000,
            'property_type': 'Land',
            'location': 'White Desert, Egypt',
            'area': 5000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 250000,
            'monthly_installment': 20833,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Garden Villa in Maadi',
            'description': 'Spacious 6-bedroom villa with extensive gardens in the diplomatic quarter of Maadi. Features mature trees, swimming pool, and separate guest quarters. Perfect for large families or diplomatic residences.',
            'price': 22000000,
            'property_type': 'Villa',
            'location': 'Maadi, Cairo',
            'area': 600.0,
            'bedrooms': 6,
            'bathrooms': 7,
            'down_payment': 2200000,
            'monthly_installment': 183333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Studio Loft in Downtown Cairo',
            'description': 'Modern studio loft in the vibrant downtown district. Features exposed brick walls, industrial design elements, and rooftop access. Perfect for young professionals or artists seeking urban living.',
            'price': 2200000,
            'property_type': 'Apartment',
            'location': 'Downtown Cairo',
            'area': 70.0,
            'bedrooms': 1,
            'bathrooms': 1,
            'down_payment': 220000,
            'monthly_installment': 18333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Commercial Land in New Capital',
            'description': 'Strategic commercial land plot in the developing New Administrative Capital. 2000 sqm corner plot with high visibility and excellent access. Perfect for retail development or office complex.',
            'price': 15000000,
            'property_type': 'Land',
            'location': 'New Administrative Capital',
            'area': 2000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 1500000,
            'monthly_installment': 125000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Mediterranean Villa in North Coast',
            'description': 'Elegant Mediterranean-style villa in the exclusive North Coast area. Features 4 bedrooms, infinity pool overlooking the sea, and private beach access. Includes landscaped gardens and outdoor entertainment areas.',
            'price': 12000000,
            'property_type': 'Villa',
            'location': 'North Coast, Egypt',
            'area': 400.0,
            'bedrooms': 4,
            'bathrooms': 4,
            'down_payment': 1200000,
            'monthly_installment': 100000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Retail Space in City Stars Mall Area',
            'description': 'High-traffic retail space near City Stars Mall. Features large display windows, modern storefront design, and excellent parking access. Perfect for fashion boutiques or specialty shops.',
            'price': 8000000,
            'property_type': 'Commercial',
            'location': 'Nasr City, Cairo',
            'area': 200.0,
            'bedrooms': 0,
            'bathrooms': 2,
            'down_payment': 800000,
            'monthly_installment': 66667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Colonial Apartment in Alexandria',
            'description': 'Restored colonial-era apartment in the historic Cecil Area of Alexandria. Features original architectural details, sea views, and proximity to the Corniche. Walking distance to cultural landmarks.',
            'price': 4200000,
            'property_type': 'Apartment',
            'location': 'Alexandria, Egypt',
            'area': 130.0,
            'bedrooms': 2,
            'bathrooms': 2,
            'down_payment': 420000,
            'monthly_installment': 35000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Industrial Land in 10th of Ramadan',
            'description': 'Large industrial land plot in the manufacturing hub of 10th of Ramadan City. 5000 sqm plot with all utilities and excellent transportation access. Perfect for factory or warehouse development.',
            'price': 8000000,
            'property_type': 'Land',
            'location': '10th of Ramadan City',
            'area': 5000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 800000,
            'monthly_installment': 66667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Golf View Villa in Sokhna',
            'description': 'Luxurious villa with golf course views in Ain Sokhna. Features 5 bedrooms, private pool, and direct access to championship golf courses. Includes membership to resort amenities and marina access.',
            'price': 14000000,
            'property_type': 'Villa',
            'location': 'Ain Sokhna, Red Sea',
            'area': 450.0,
            'bedrooms': 5,
            'bathrooms': 5,
            'down_payment': 1400000,
            'monthly_installment': 116667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Art Gallery Space in Zamalek',
            'description': 'Charming gallery space in the artistic district of Zamalek. Features high ceilings, natural light, and exposed brick walls. Perfect for contemporary art galleries or design studios.',
            'price': 6500000,
            'property_type': 'Commercial',
            'location': 'Zamalek, Cairo',
            'area': 150.0,
            'bedrooms': 0,
            'bathrooms': 2,
            'down_payment': 650000,
            'monthly_installment': 54167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Mountain Land in Saint Catherine',
            'description': 'Spectacular mountain land plot at the foot of Mount Sinai. 3000 sqm plot with breathtaking views and proximity to ancient monasteries. Perfect for eco-tourism development or spiritual retreat center.',
            'price': 3200000,
            'property_type': 'Land',
            'location': 'Saint Catherine, Sinai',
            'area': 3000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 320000,
            'monthly_installment': 26667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Palatial Villa in Heliopolis',
            'description': 'Grand palatial villa in the royal district of Heliopolis. Features 7 bedrooms, ballroom, multiple living areas, and extensive gardens. Perfect for large-scale entertaining or diplomatic residences.',
            'price': 35000000,
            'property_type': 'Villa',
            'location': 'Heliopolis, Cairo',
            'area': 800.0,
            'bedrooms': 7,
            'bathrooms': 8,
            'down_payment': 3500000,
            'monthly_installment': 291667,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Loft Apartment in Dokki',
            'description': 'Industrial-style loft apartment in the trendy Dokki district. Features exposed concrete ceilings, large windows, and modern industrial design. Perfect for creative professionals and young urbanites.',
            'price': 2800000,
            'property_type': 'Apartment',
            'location': 'Dokki, Giza',
            'area': 100.0,
            'bedrooms': 1,
            'bathrooms': 1,
            'down_payment': 280000,
            'monthly_installment': 23333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Agricultural Land in Minya',
            'description': 'Productive agricultural land along the Nile River in Minya. 4000 sqm plot with fertile soil and irrigation access. Suitable for various crops and agricultural investment opportunities.',
            'price': 2400000,
            'property_type': 'Land',
            'location': 'Minya, Egypt',
            'area': 4000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 240000,
            'monthly_installment': 20000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Beachfront Villa in Dahab',
            'description': 'Peaceful beachfront villa in the laid-back town of Dahab. Features 3 bedrooms, direct beach access, and traditional Bedouin architecture. Perfect for those seeking tranquility and water sports activities.',
            'price': 5800000,
            'property_type': 'Villa',
            'location': 'Dahab, Sinai',
            'area': 300.0,
            'bedrooms': 3,
            'bathrooms': 3,
            'down_payment': 580000,
            'monthly_installment': 48333,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Restaurant Space in Khan El Khalili',
            'description': 'Historic restaurant space in the bustling Khan El Khalili bazaar. Features traditional Islamic architecture, courtyard seating, and authentic local ambiance. Perfect for traditional Egyptian cuisine or tourist-oriented dining.',
            'price': 7200000,
            'property_type': 'Commercial',
            'location': 'Khan El Khalili, Cairo',
            'area': 180.0,
            'bedrooms': 0,
            'bathrooms': 4,
            'down_payment': 720000,
            'monthly_installment': 60000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Desert Land in Bahariya Oasis',
            'description': 'Expansive desert land plot in the fertile Bahariya Oasis. 6000 sqm plot surrounded by palm groves and natural springs. Perfect for organic farming or eco-tourism development.',
            'price': 1800000,
            'property_type': 'Land',
            'location': 'Bahariya Oasis, Egypt',
            'area': 6000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 180000,
            'monthly_installment': 15000,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Sky Villa in Mountain View',
            'description': 'Spectacular sky villa with panoramic mountain views in the Eastern Desert. Features 4 bedrooms, infinity pool, and glass-walled living areas. Includes solar power and water collection systems.',
            'price': 9500000,
            'property_type': 'Villa',
            'location': 'Eastern Desert, Egypt',
            'area': 350.0,
            'bedrooms': 4,
            'bathrooms': 4,
            'down_payment': 950000,
            'monthly_installment': 79167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Boutique Hotel in Luxor',
            'description': 'Intimate boutique hotel in the heart of Luxor. Features 12 elegantly decorated rooms, Nile River views, and traditional Nubian architecture. Includes restaurant and rooftop terrace overlooking the temples.',
            'price': 18500000,
            'property_type': 'Commercial',
            'location': 'Luxor, Egypt',
            'area': 600.0,
            'bedrooms': 12,
            'bathrooms': 14,
            'down_payment': 1850000,
            'monthly_installment': 154167,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Eco-Lodge Land in Ras Mohammed',
            'description': 'Prime land plot in the protected Ras Mohammed National Park. 4000 sqm plot with coral reef views and marine biodiversity. Perfect for developing an eco-lodge or research facility.',
            'price': 4500000,
            'property_type': 'Land',
            'location': 'Ras Mohammed, Sinai',
            'area': 4000.0,
            'bedrooms': 0,
            'bathrooms': 0,
            'down_payment': 450000,
            'monthly_installment': 37500,
            'installment_years': 10,
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
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
