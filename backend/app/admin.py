import os
from flask_admin import Admin
from .db import db
from .models import User
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Charity Directory Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    # Add more models as needed
    # admin.add_view(ModelView(YourModelName, db.session))
