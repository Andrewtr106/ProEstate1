from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from config import Config
from models import db, Property, ContactMessage, User, Favorite
from forms import PropertyForm, ContactForm, LoginForm, RegisterForm, ProfileForm, UserPropertyForm
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    # Initialize database
    db.init_app(app)

    # Create necessary folders
    with app.app_context():
        os.makedirs('static/uploads', exist_ok=True)
        os.makedirs('static/images/properties', exist_ok=True)

    return app

app = create_app()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password.', 'error')
        except Exception as e:
            print(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', 'error')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('register.html', form=form)

            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data or None
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash('Registration successful! Please login to continue.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        try:
            # Verify current password
            if not current_user.check_password(form.current_password.data):
                flash('Current password is incorrect.', 'error')
                return render_template('profile.html', form=form)

            # Update user information
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data

            # Update password if provided
            if form.new_password.data:
                current_user.set_password(form.new_password.data)

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            print(f"Profile update error: {str(e)}")
            flash('An error occurred while updating your profile. Please try again.', 'error')

    return render_template('profile.html', form=form)

@app.route('/add-property', methods=['GET', 'POST'])
@login_required
def user_add_property():
    form = UserPropertyForm()
    if form.validate_on_submit():
        try:
            # Handle image upload
            image_filename = None
            if form.image.data:
                image_file = form.image.data
                # Generate unique filename
                import uuid
                image_filename = str(uuid.uuid4()) + '_' + image_file.filename
                image_path = os.path.join(app.root_path, 'static', 'uploads', image_filename)
                image_file.save(image_path)

            property_item = Property(
                title=form.title.data,
                description=form.description.data,
                price=form.price.data,
                property_type=form.property_type.data,
                location=form.location.data,
                area=form.area.data,
                bedrooms=form.bedrooms.data or 0,
                bathrooms=form.bathrooms.data or 0,
                down_payment=form.down_payment.data,
                monthly_installment=form.monthly_installment.data,
                installment_years=form.installment_years.data,
                image=image_filename,
                user_id=current_user.id
            )

            db.session.add(property_item)
            db.session.commit()
            flash('Property added successfully!', 'success')
            return redirect(url_for('my_properties'))
        except Exception as e:
            db.session.rollback()
            print(f"Error in user_add_property: {str(e)}")
            flash('An error occurred while adding the property. Please try again.', 'error')

    return render_template('user/add_property.html', form=form)

@app.route('/my-properties')
@login_required
def my_properties():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10

        properties_pagination = Property.query.filter_by(user_id=current_user.id)\
            .order_by(Property.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return render_template('my_properties.html',
                             properties=properties_pagination.items,
                             pagination=properties_pagination)
    except Exception as e:
        print(f"Error in my_properties: {str(e)}")
        flash('An error occurred while loading your properties.', 'error')
        return render_template('my_properties.html', properties=[])

@app.route('/favorites')
@login_required
def favorites():
    try:
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        property_ids = [f.property_id for f in favorites]
        properties = Property.query.filter(Property.id.in_(property_ids)).all()

        return render_template('favorites.html', properties=properties)
    except Exception as e:
        print(f"Error in favorites: {str(e)}")
        flash('An error occurred while loading your favorites.', 'error')
        return render_template('favorites.html', properties=[])

@app.route('/check-favorite/<int:property_id>')
@login_required
def check_favorite(property_id):
    try:
        favorite = Favorite.query.filter_by(user_id=current_user.id, property_id=property_id).first()
        return jsonify({'is_favorited': favorite is not None})
    except Exception as e:
        print(f"Error in check_favorite: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/toggle-favorite/<int:property_id>', methods=['POST'])
@login_required
def toggle_favorite(property_id):
    try:
        favorite = Favorite.query.filter_by(user_id=current_user.id, property_id=property_id).first()

        if favorite:
            # Remove from favorites
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'success': True, 'is_favorited': False, 'message': 'Removed from favorites'})
        else:
            # Add to favorites
            new_favorite = Favorite(user_id=current_user.id, property_id=property_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({'success': True, 'is_favorited': True, 'message': 'Added to favorites'})
    except Exception as e:
        db.session.rollback()
        print(f"Error in toggle_favorite: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# Main routes
@app.route('/')
def index():
    try:
        featured_properties = Property.query.filter_by(status='available')\
            .order_by(Property.created_at.desc())\
            .limit(6)\
            .all()
        return render_template('index.html', 
                             featured_properties=featured_properties,
                             site_name=Config.SITE_NAME)
    except Exception as e:
        print(f"Error in index: {str(e)}")
        flash('An error occurred while loading the homepage.', 'error')
        return render_template('index.html', featured_properties=[])

@app.route('/about')
def about():
    return render_template('about.html', site_name=Config.SITE_NAME)

@app.route('/properties')
def properties():
    try:
        property_type = request.args.get('type', '')
        location = request.args.get('location', '')
        page = request.args.get('page', 1, type=int)

        query = Property.query.filter_by(status='available')

        if property_type:
            query = query.filter_by(property_type=property_type)
        if location:
            query = query.filter(Property.location.contains(location))

        # Pagination: 5 properties per page
        properties_pagination = query.order_by(Property.created_at.desc()).paginate(
            page=page, per_page=5, error_out=False
        )

        return render_template('properties.html',
                             properties=properties_pagination.items,
                             pagination=properties_pagination,
                             search_type=property_type,
                             search_location=location)
    except Exception as e:
        print(f"Error in properties: {str(e)}")
        flash('An error occurred while loading properties.', 'error')
        return render_template('properties.html', properties=[])

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    try:
        property_item = Property.query.get_or_404(property_id)
        
        similar_properties = Property.query.filter(
            Property.property_type == property_item.property_type,
            Property.id != property_id,
            Property.status == 'available'
        ).limit(3).all()
        
        return render_template('property_detail.html', 
                             property=property_item,
                             similar_properties=similar_properties)
    except Exception as e:
        print(f"Error in property_detail: {str(e)}")
        flash('The requested property was not found.', 'error')
        return redirect(url_for('properties'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    property_id = request.args.get('property', type=int)
    
    if form.validate_on_submit():
        try:
            message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data or '',
                subject=form.subject.data or '',
                message=form.message.data,
                property_id=property_id
            )
            db.session.add(message)
            db.session.commit()
            flash('Your message has been sent successfully! We will contact you soon.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            print(f"Error in contact: {str(e)}")
            flash('An error occurred while sending your message. Please try again.', 'error')
    
    return render_template('contact.html', form=form, property_id=property_id)

# Admin routes
@app.route('/admin/add-property', methods=['GET', 'POST'])
@login_required
def add_property():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))

    form = PropertyForm()
    if form.validate_on_submit():
        try:
            # Handle image upload
            image_filename = None
            if form.image.data:
                image_file = form.image.data
                # Generate unique filename
                import uuid
                image_filename = str(uuid.uuid4()) + '_' + image_file.filename
                image_path = os.path.join(app.root_path, 'static', 'uploads', image_filename)
                image_file.save(image_path)

            property_item = Property(
                title=form.title.data,
                description=form.description.data,
                price=form.price.data,
                property_type=form.property_type.data,
                location=form.location.data,
                area=form.area.data,
                bedrooms=form.bedrooms.data or 0,
                bathrooms=form.bathrooms.data or 0,
                down_payment=form.down_payment.data,
                monthly_installment=form.monthly_installment.data,
                installment_years=form.installment_years.data,
                image=image_filename
            )

            db.session.add(property_item)
            db.session.commit()
            flash('Property added successfully!', 'success')
            return redirect(url_for('admin_properties'))
        except Exception as e:
            db.session.rollback()
            print(f"Error in add_property: {str(e)}")
            flash('An error occurred while adding the property. Please try again.', 'error')

    return render_template('admin/add_property.html', form=form)

@app.route('/admin/properties')
@login_required
def admin_properties():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))

    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Show 10 properties per page for admin

        # Get pagination object
        properties_pagination = Property.query.order_by(Property.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return render_template('admin/properties.html',
                             properties=properties_pagination.items,
                             pagination=properties_pagination)
    except Exception as e:
        print(f"Error in admin_properties: {str(e)}")
        flash('An error occurred while loading properties.', 'error')
        return render_template('admin/properties.html', properties=[])

@app.route('/admin/edit-property/<int:property_id>', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))

    property_item = Property.query.get_or_404(property_id)
    form = PropertyForm(obj=property_item)

    if form.validate_on_submit():
        try:
            # Handle image upload
            if form.image.data:
                image_file = form.image.data
                # Generate unique filename
                import uuid
                image_filename = str(uuid.uuid4()) + '_' + image_file.filename
                image_path = os.path.join(app.root_path, 'static', 'uploads', image_filename)
                image_file.save(image_path)
                property_item.image = image_filename

            property_item.title = form.title.data
            property_item.description = form.description.data
            property_item.price = form.price.data
            property_item.property_type = form.property_type.data
            property_item.location = form.location.data
            property_item.area = form.area.data
            property_item.bedrooms = form.bedrooms.data or 0
            property_item.bathrooms = form.bathrooms.data or 0
            property_item.down_payment = form.down_payment.data
            property_item.monthly_installment = form.monthly_installment.data
            property_item.installment_years = form.installment_years.data

            db.session.commit()
            flash('Property updated successfully!', 'success')
            return redirect(url_for('admin_properties'))
        except Exception as e:
            db.session.rollback()
            print(f"Error in edit_property: {str(e)}")
            flash('An error occurred while updating the property. Please try again.', 'error')

    return render_template('admin/edit_property.html', form=form, property=property_item)

@app.route('/admin/delete-property/<int:property_id>', methods=['POST'])
@login_required
def delete_property(property_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))

    try:
        property_item = Property.query.get_or_404(property_id)
        db.session.delete(property_item)
        db.session.commit()
        flash('Property deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error in delete_property: {str(e)}")
        flash('An error occurred while deleting the property. Please try again.', 'error')

    return redirect(url_for('admin_properties'))



# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
