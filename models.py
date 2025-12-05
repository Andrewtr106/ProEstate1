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
        self._is_active = is_active
        self.is_admin = is_admin

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

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
        # Check if user already exists
        existing_user = cls.get_by_email(email)
        if existing_user:
            return existing_user

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
        result = cursor.fetchone()
        if result and result[0] is not None:
            user.id = int(result[0])
        else:
            # Check if user was actually inserted
            cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
            check_result = cursor.fetchone()
            if check_result and check_result[0] is not None:
                user.id = int(check_result[0])
            else:
                raise Exception("Failed to create user - no ID returned from database and user not found")
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
        try:
            db_conn.cursor.execute(query, (
                prop.title, prop.description, prop.price, prop.property_type, prop.location, prop.area,
                prop.bedrooms, prop.bathrooms, prop.down_payment, prop.monthly_installment,
                prop.installment_years, prop.image, prop.created_at, prop.updated_at, prop.status, prop.user_id
            ))

            db_conn.cursor.execute("SELECT SCOPE_IDENTITY() AS id")
            result = db_conn.cursor.fetchone()
            if result and result[0] is not None:
                prop.id = int(result[0])
            else:
                # Try @@IDENTITY as fallback
                db_conn.cursor.execute("SELECT @@IDENTITY AS id")
                result = db_conn.cursor.fetchone()
                if result and result[0] is not None:
                    prop.id = int(result[0])
                else:
                    raise Exception("Failed to create property - no ID returned from database")

            db_conn.commit()
            return prop
        except Exception as e:
            db_conn.rollback()
            raise e

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
    def get_featured(cls, limit=6):
        query = "SELECT TOP (?) * FROM properties WHERE status = 'available' ORDER BY created_at DESC"
        conn, cursor = db_conn.execute_query(query, (limit,))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        return [cls(*row) for row in rows]

    @classmethod
    def get_available(cls, property_type='', location='', page=1, per_page=5):
        from math import ceil

        # Build query with filters
        query = "SELECT * FROM properties WHERE status = 'available'"
        params = []

        if property_type:
            query += " AND property_type = ?"
            params.append(property_type)

        if location:
            query += " AND location LIKE ?"
            params.append(f'%{location}%')

        query += " ORDER BY created_at DESC"

        # Get total count for pagination
        count_query = f"SELECT COUNT(*) FROM properties WHERE status = 'available'"
        count_params = []
        if property_type:
            count_query += " AND property_type = ?"
            count_params.append(property_type)
        if location:
            count_query += " AND location LIKE ?"
            count_params.append(f'%{location}%')

        conn, cursor = db_conn.execute_query(count_query, count_params)
        total_count = cursor.fetchone()[0]
        db_conn.close_connection(conn, cursor)

        # Add pagination
        offset = (page - 1) * per_page
        query += " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        params.extend([offset, per_page])

        conn, cursor = db_conn.execute_query(query, params)
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)

        # Create pagination object
        class Pagination:
            def __init__(self, items, page, per_page, total):
                self.items = items
                self.page = page
                self.per_page = per_page
                self.total = total
                self.pages = ceil(total / per_page)

            def has_prev(self):
                return self.page > 1

            def has_next(self):
                return self.page < self.pages

            def prev_num(self):
                return self.page - 1

            def next_num(self):
                return self.page + 1

            def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
                """Iterate over the page numbers in the pagination."""
                last = 0
                for num in range(1, self.pages + 1):
                    if num <= left_edge or \
                       (num > self.page - left_current - 1 and \
                        num < self.page + right_current) or \
                       num > self.pages - right_edge:
                        if last + 1 != num:
                            yield None
                        yield num
                        last = num

        return Pagination([cls(*row) for row in rows], page, per_page, total_count)

    @classmethod
    def get_all_paginated(cls, page=1, per_page=10):
        from math import ceil

        # Get total count
        count_query = "SELECT COUNT(*) FROM properties"
        conn, cursor = db_conn.execute_query(count_query)
        total_count = cursor.fetchone()[0]
        db_conn.close_connection(conn, cursor)

        # Get paginated results
        offset = (page - 1) * per_page
        query = "SELECT * FROM properties ORDER BY created_at DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        conn, cursor = db_conn.execute_query(query, (offset, per_page))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)

        # Create pagination object
        class Pagination:
            def __init__(self, items, page, per_page, total):
                self.items = items
                self.page = page
                self.per_page = per_page
                self.total = total
                self.pages = ceil(total / per_page)

            def has_prev(self):
                return self.page > 1

            def has_next(self):
                return self.page < self.pages

            def prev_num(self):
                return self.page - 1

            def next_num(self):
                return self.page + 1

            def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
                """Iterate over the page numbers in the pagination."""
                last = 0
                for num in range(1, self.pages + 1):
                    if num <= left_edge or \
                       (num > self.page - left_current - 1 and \
                        num < self.page + right_current) or \
                       num > self.pages - right_edge:
                        if last + 1 != num:
                            yield None
                        yield num
                        last = num

        return Pagination([cls(*row) for row in rows], page, per_page, total_count)

    @classmethod
    def get_by_user_paginated(cls, user_id, page=1, per_page=10):
        from math import ceil

        # Get total count for user
        count_query = "SELECT COUNT(*) FROM properties WHERE user_id = ?"
        conn, cursor = db_conn.execute_query(count_query, (user_id,))
        total_count = cursor.fetchone()[0]
        db_conn.close_connection(conn, cursor)

        # Get paginated results for user
        offset = (page - 1) * per_page
        query = "SELECT * FROM properties WHERE user_id = ? ORDER BY created_at DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        conn, cursor = db_conn.execute_query(query, (user_id, offset, per_page))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)

        # Create pagination object
        class Pagination:
            def __init__(self, items, page, per_page, total):
                self.items = items
                self.page = page
                self.per_page = per_page
                self.total = total
                self.pages = ceil(total / per_page)

            def has_prev(self):
                return self.page > 1

            def has_next(self):
                return self.page < self.pages

            def prev_num(self):
                return self.page - 1

            def next_num(self):
                return self.page + 1

            def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
                """Iterate over the page numbers in the pagination."""
                last = 0
                for num in range(1, self.pages + 1):
                    if num <= left_edge or \
                       (num > self.page - left_current - 1 and \
                        num < self.page + right_current) or \
                       num > self.pages - right_edge:
                        if last + 1 != num:
                            yield None
                        yield num
                        last = num

        return Pagination([cls(*row) for row in rows], page, per_page, total_count)

    @classmethod
    def get_similar(cls, property_id, property_type, limit=3):
        query = """
        SELECT TOP (?) * FROM properties
        WHERE property_type = ? AND id != ? AND status = 'available'
        ORDER BY created_at DESC
        """
        conn, cursor = db_conn.execute_query(query, (limit, property_type, property_id))
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
        try:
            db_conn.cursor.execute(query, (fav.user_id, fav.property_id, fav.created_at))

            db_conn.cursor.execute("SELECT SCOPE_IDENTITY() AS id")
            result = db_conn.cursor.fetchone()
            if result and result[0] is not None:
                fav.id = int(result[0])
            else:
                # Try @@IDENTITY as fallback
                db_conn.cursor.execute("SELECT @@IDENTITY AS id")
                result = db_conn.cursor.fetchone()
                if result and result[0] is not None:
                    fav.id = int(result[0])
                else:
                    raise Exception("Failed to create favorite - no ID returned from database")

            db_conn.commit()
            return fav
        except Exception as e:
            db_conn.rollback()
            raise e

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

    @classmethod
    def get_by_user_and_property(cls, user_id, property_id):
        query = "SELECT * FROM favorites WHERE user_id = ? AND property_id = ?"
        conn, cursor = db_conn.execute_query(query, (user_id, property_id))
        row = cursor.fetchone()
        db_conn.close_connection(conn, cursor)
        if row:
            return cls(*row)
        return None

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
        try:
            db_conn.cursor.execute(query, (
                msg.name, msg.email, msg.phone, msg.subject, msg.message, msg.property_id,
                msg.created_at, msg.is_read
            ))

            db_conn.cursor.execute("SELECT SCOPE_IDENTITY() AS id")
            result = db_conn.cursor.fetchone()
            if result and result[0] is not None:
                msg.id = int(result[0])
            else:
                # Try @@IDENTITY as fallback
                db_conn.cursor.execute("SELECT @@IDENTITY AS id")
                result = db_conn.cursor.fetchone()
                if result and result[0] is not None:
                    msg.id = int(result[0])
                else:
                    raise Exception("Failed to create contact message - no ID returned from database")

            db_conn.commit()
            return msg
        except Exception as e:
            db_conn.rollback()
            raise e

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

class ChatHistory:
    def __init__(self, id=None, user_id=None, timestamp=None, role=None, message=None):
        self.id = id
        self.user_id = user_id
        self.timestamp = timestamp or datetime.utcnow()
        self.role = role  # 'user' or 'assistant'
        self.message = message

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'role': self.role,
            'message': self.message
        }

    def __repr__(self):
        return f'<ChatHistory {self.role}: {self.message[:50]}...>'

    @classmethod
    def create(cls, user_id, role, message):
        chat = cls(user_id=user_id, role=role, message=message)

        query = """
        INSERT INTO chat_history (user_id, timestamp, role, message)
        VALUES (?, ?, ?, ?)
        """
        try:
            db_conn.cursor.execute(query, (
                chat.user_id, chat.timestamp, chat.role, chat.message
            ))

            db_conn.cursor.execute("SELECT SCOPE_IDENTITY() AS id")
            result = db_conn.cursor.fetchone()
            if result and result[0] is not None:
                chat.id = int(result[0])
            else:
                # Try @@IDENTITY as fallback
                db_conn.cursor.execute("SELECT @@IDENTITY AS id")
                result = db_conn.cursor.fetchone()
                if result and result[0] is not None:
                    chat.id = int(result[0])
                else:
                    raise Exception("Failed to create chat history - no ID returned from database")

            db_conn.commit()
            return chat
        except Exception as e:
            db_conn.rollback()
            raise e

    @classmethod
    def get_by_user_id(cls, user_id, limit=50):
        query = "SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC"
        if limit:
            query += f" OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"
        conn, cursor = db_conn.execute_query(query, (user_id,))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        # Return in chronological order (oldest first)
        return [cls(*row) for row in reversed(rows)]

    @classmethod
    def get_recent_by_user(cls, user_id, limit=20):
        """Get recent messages for conversation context"""
        query = """
        SELECT TOP (?) * FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        """
        conn, cursor = db_conn.execute_query(query, (limit, user_id))
        rows = cursor.fetchall()
        db_conn.close_connection(conn, cursor)
        # Return in chronological order
        return [cls(*row) for row in reversed(rows)]

    @classmethod
    def delete_old_messages(cls, user_id, keep_last=100):
        """Delete old messages keeping only the most recent ones"""
        query = """
        DELETE FROM chat_history
        WHERE user_id = ? AND id NOT IN (
            SELECT TOP (?) id FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
        )
        """
        conn, cursor = db_conn.execute_non_query(query, (user_id, keep_last, user_id))
        db_conn.close_connection(conn, cursor)

    def delete(self):
        query = "DELETE FROM chat_history WHERE id=?"
        conn, cursor = db_conn.execute_non_query(query, (self.id,))
        db_conn.close_connection(conn, cursor)


