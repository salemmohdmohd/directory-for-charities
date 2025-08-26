import os
from flask_admin import Admin
from .db import db
from .models import User
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, BooleanField, SelectField, TextAreaField
from flask_admin.form import BaseForm

class UserForm(BaseForm):
    name = StringField('Name')
    email = StringField('Email')
    password_hash = StringField('Password Hash')
    role = SelectField('Role', choices=[('visitor', 'Visitor'), ('admin', 'Admin')])
    is_verified = BooleanField('Is Verified')
    google_id = StringField('Google ID')
    profile_picture = StringField('Profile Picture')

class UserModelView(ModelView):
    form = UserForm
    column_list = ['user_id', 'name', 'email', 'role', 'is_verified']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Charity Directory Admin', template_mode='bootstrap3')

    # Use custom form to avoid tuple error
    admin.add_view(UserModelView(User, db.session, name='Users'))
    from .models import Organization, Category, Location, Notification, AuditLog, Advertisement
    admin.add_view(ModelView(Organization, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Location, db.session))
    admin.add_view(ModelView(Notification, db.session))
    admin.add_view(ModelView(AuditLog, db.session))
    admin.add_view(ModelView(Advertisement, db.session))
