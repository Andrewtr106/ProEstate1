from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    properties = db.relationship('Property', backref='owner', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return f'<User {self.email}>'

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    area = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Integer, default=0)
    down_payment = db.Column(db.Float)
    monthly_installment = db.Column(db.Float)
    installment_years = db.Column(db.Integer)
    image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='available')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # For user-added properties
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'property_type': self.property_type,
            'location': self.location,
            'area': self.area,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'down_payment': self.down_payment,
            'monthly_installment': self.monthly_installment,
            'installment_years': self.installment_years,
            'image': self.image,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'status': self.status
        }
    
    def __repr__(self):
        return f'<Property {self.title}>'

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    property = db.relationship('Property', backref=db.backref('favorited_by', lazy=True))

    def __repr__(self):
        return f'<Favorite User:{self.user_id} Property:{self.property_id}>'

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    property = db.relationship('Property', backref=db.backref('inquiries', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'property_id': self.property_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read
        }

    def __repr__(self):
        return f'<ContactMessage {self.name}>'


