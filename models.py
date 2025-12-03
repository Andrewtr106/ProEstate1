from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from db_utils import DatabaseConnection

db_conn = DatabaseConnection()

class User(UserMixin):
    def __init__(self, id=None, email=None, password_hash=None, first_name=None, last_name=None,
                 phone=None, created_at=None, is_active=True, is_admin=False):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.created_at = created_at or datetime.utcnow()
        self.is_active = is_active
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

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

    @classmethod
    def create(cls, email, first_name, last_name, phone, password=None, is_admin=False):
        user = cls(email=email, first_name=first_name, last_name=last_name, phone=phone, is_admin=is_admin)
        if password:
            user.set_password(password)

        query = """
        INSERT INTO users (email, password_hash, first_name, last_name, phone, created_at, is_active, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn, cursor = db_conn.execute_non_query(query, (
            user.email, user.password_hash, user.first_name, user.last_name, user.phone,
            user.created_at, user.is_active, user.is_admin
        ))

        cursor.execute("SELECT SCOPE_IDENTITY()")
        user.id = int(cursor.fetchone()[0])
        db_conn.close_connection(conn, cursor)
        return user

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = ?"
        conn, cursor = db_conn.execute_query(query, (user_id,))
        row = cursor.fetchone()
        db_conn.close_connection(conn, cursor)
        if row:
            return cls(*row)
        return None

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = ?"
        conn, cursor = db_conn.execute_query(query, (email,))
        row = cursor.fetchone()
        db_conn.close_connection(conn, cursor)
        if row:
            return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query)
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    def update(self):
        query = """
        UPDATE users SET email=?, password_hash=?, first_name=?, last_name=?, phone=?, is_active=?, is_admin=?
        WHERE id=?
        """
        conn, cursor = db_conn.execute_non_query(query, (
            self.email, self.password_hash, self.first_name, self.last_name, self.phone,
            self.is_active, self.is_admin, self.id
        ))
        db_conn.close_connection(conn, cursor)

    def delete(self):
        query = "DELETE FROM users WHERE id=?"
        conn, cursor = db_conn.execute_non_query(query, (self.id,))
        db_conn.close_connection(conn, cursor)

    def get_properties(self):
        return Property.get_by_user_id(self.id)

    def get_favorites(self):
        return Favorite.get_by_user_id(self.id)

class Property:
    def __init__(self, id=None, title=None, description=None, price=None, property_type=None,
                 location=None, area=None, bedrooms=0, bathrooms=0, down_payment=None,
                 monthly_installment=None, installment_years=None, image=None, created_at=None,
                 updated_at=None, status='available', user_id=None):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.property_type = property_type
        self.location = location
        self.area = area
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.down_payment = down_payment
        self.monthly_installment = monthly_installment
        self.installment_years = installment_years
        self.image = image
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at
        self.status = status
        self.user_id = user_id

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

    @classmethod
    def create(cls, title, description, price, property_type, location, area, bedrooms=0,
               bathrooms=0, down_payment=None, monthly_installment=None, installment_years=None,
               image=None, user_id=None):
        prop = cls(title=title, description=description, price=price, property_type=property_type,
                   location=location, area=area, bedrooms=bedrooms, bathrooms=bathrooms,
                   down_payment=down_payment, monthly_installment=monthly_installment,
                   installment_years=installment_years, image=image, user_id=user_id)

        query = """
        INSERT INTO properties (title, description, price, property_type, location, area, bedrooms,
                               bathrooms, down_payment, monthly_installment, installment_years, image,
                               created_at, updated_at, status, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn, cursor = db_conn.execute_non_query(query, (
            prop.title, prop.description, prop.price, prop.property_type, prop.location, prop.area,
            prop.bedrooms, prop.bathrooms, prop.down_payment, prop.monthly_installment,
            prop.installment_years, prop.image, prop.created_at, prop.updated_at, prop.status, prop.user_id
        ))

        cursor.execute("SELECT SCOPE_IDENTITY()")
        prop.id = int(cursor.fetchone()[0])
        db_conn.close_connection(conn, cursor)
        return prop

    @classmethod
    def get_by_id(cls, prop_id):
        query = "SELECT * FROM properties WHERE id = ?"
        conn, cursor = db_conn.execute_query(query, (prop_id,))
        row = cursor.fetchone()
        db_conn.close_connection(conn, cursor)
        if row:
            return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM properties ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query)
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM properties WHERE user_id = ? ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query, (user_id,))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_status(cls, status):
        query = "SELECT * FROM properties WHERE status = ? ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query, (status,))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_title(cls, title):
        query = "SELECT * FROM properties WHERE title = ?"
        conn, cursor = db_conn.execute_query(query, (title,))
        row = cursor.fetchone()
        db_conn.close_connection(conn, cursor)
        if row:
            return cls(*row)
        return None

    def update(self):
        self.updated_at = datetime.utcnow()
        query = """
        UPDATE properties SET title=?, description=?, price=?, property_type=?, location=?, area=?,
                             bedrooms=?, bathrooms=?, down_payment=?, monthly_installment=?,
                             installment_years=?, image=?, updated_at=?, status=?, user_id=?
        WHERE id=?
        """
        conn, cursor = db_conn.execute_non_query(query, (
            self.title, self.description, self.price, self.property_type, self.location, self.area,
            self.bedrooms, self.bathrooms, self.down_payment, self.monthly_installment,
            self.installment_years, self.image, self.updated_at, self.status, self.user_id, self.id
        ))
        db_conn.close_connection(conn, cursor)

    def delete(self):
        query = "DELETE FROM properties WHERE id=?"
        conn, cursor = db_conn.execute_non_query(query, (self.id,))
        db_conn.close_connection(conn, cursor)

    def get_owner(self):
        if self.user_id:
            return User.get_by_id(self.user_id)
        return None

class Favorite:
    def __init__(self, id=None, user_id=None, property_id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.property_id = property_id
        self.created_at = created_at or datetime.utcnow()

    def __repr__(self):
        return f'<Favorite User:{self.user_id} Property:{self.property_id}>'

    @classmethod
    def create(cls, user_id, property_id):
        fav = cls(user_id=user_id, property_id=property_id)

        query = "INSERT INTO favorites (user_id, property_id, created_at) VALUES (?, ?, ?)"
        conn, cursor = db_conn.execute_non_query(query, (fav.user_id, fav.property_id, fav.created_at))

        cursor.execute("SELECT SCOPE_IDENTITY()")
        fav.id = int(cursor.fetchone()[0])
        db_conn.close_connection(conn, cursor)
        return fav

    @classmethod
    def get_by_id(cls, fav_id):
        query = "SELECT * FROM favorites WHERE id = ?"
        conn, cursor = db_conn.execute_query(query, (fav_id,))
        row = cursor.fetchone()
        db_conn.close_connection(conn, cursor)
        if row:
            return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM favorites ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query)
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM favorites WHERE user_id = ? ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query, (user_id,))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_property_id(cls, property_id):
        query = "SELECT * FROM favorites WHERE property_id = ? ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query, (property_id,))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    def update(self):
        # Favorites don't have updatable fields besides timestamps, but keeping for consistency
        pass

    def delete(self):
        query = "DELETE FROM favorites WHERE id=?"
        conn, cursor = db_conn.execute_non_query(query, (self.id,))
        db_conn.close_connection(conn, cursor)

    def get_user(self):
        return User.get_by_id(self.user_id)

    def get_property(self):
        return Property.get_by_id(self.property_id)

class ContactMessage:
    def __init__(self, id=None, name=None, email=None, phone=None, subject=None, message=None,
                 property_id=None, created_at=None, is_read=False):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.subject = subject
        self.message = message
        self.property_id = property_id
        self.created_at = created_at or datetime.utcnow()
        self.is_read = is_read

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

    @classmethod
    def create(cls, name, email, phone, subject, message, property_id=None):
        msg = cls(name=name, email=email, phone=phone, subject=subject, message=message,
                  property_id=property_id)

        query = """
        INSERT INTO contact_messages (name, email, phone, subject, message, property_id, created_at, is_read)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn, cursor = db_conn.execute_non_query(query, (
            msg.name, msg.email, msg.phone, msg.subject, msg.message, msg.property_id,
            msg.created_at, msg.is_read
        ))

        cursor.execute("SELECT SCOPE_IDENTITY()")
        msg.id = int(cursor.fetchone()[0])
        db_conn.close_connection(conn, cursor)
        return msg

    @classmethod
    def get_by_id(cls, msg_id):
        query = "SELECT * FROM contact_messages WHERE id = ?"
        conn, cursor = db_conn.execute_query(query, (msg_id,))
        row = cursor.fetchone()
        db_conn.close_connection(conn, cursor)
        if row:
            return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM contact_messages ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query)
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_property_id(cls, property_id):
        query = "SELECT * FROM contact_messages WHERE property_id = ? ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query, (property_id,))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    def update(self):
        query = """
        UPDATE contact_messages SET name=?, email=?, phone=?, subject=?, message=?, property_id=?, is_read=?
        WHERE id=?
        """
        conn, cursor = db_conn.execute_non_query(query, (
            self.name, self.email, self.phone, self.subject, self.message, self.property_id,
            self.is_read, self.id
        ))
        db_conn.close_connection(conn, cursor)

    def delete(self):
        query = "DELETE FROM contact_messages WHERE id=?"
        conn, cursor = db_conn.execute_non_query(query, (self.id,))
        db_conn.close_connection(conn, cursor)

    def get_property(self):
        if self.property_id:
            return Property.get_by_id(self.property_id)
        return None


