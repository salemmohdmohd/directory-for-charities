import os
from datetime import datetime, timedelta
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from wtforms import StringField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash
from flask_admin.form import BaseForm
from .db import db
from .models import User

class DashboardView(AdminIndexView):
    """Custom admin home dashboard with statistics and quick actions"""

    @expose('/')
    def index(self):
        # Get dashboard statistics
        stats = self.get_dashboard_stats()
        recent_activity = self.get_recent_activity()
        return self.render('admin/dashboard.html',
                         stats=stats,
                         recent_activity=recent_activity)

    def get_dashboard_stats(self):
        """Calculate key metrics for the dashboard"""
        try:
            from .models import Organization, Category, Location

            # Get counts
            total_users = User.query.count()
            total_orgs = Organization.query.count() if hasattr(Organization, 'query') else 0
            verified_users = User.query.filter_by(is_verified=True).count()
            admin_users = User.query.filter_by(role='admin').count()

            # Get recent activity (last 7 days)
            week_ago = datetime.now() - timedelta(days=7)
            new_users_week = User.query.filter(User.created_at >= week_ago).count() if hasattr(User, 'created_at') else 0

            return {
                'total_users': total_users,
                'total_organizations': total_orgs,
                'verified_users': verified_users,
                'admin_users': admin_users,
                'new_users_this_week': new_users_week,
                'verification_rate': round((verified_users / total_users * 100) if total_users > 0 else 0, 1)
            }
        except Exception as e:
            # Return default stats if there's an error
            return {
                'total_users': 0,
                'total_organizations': 0,
                'verified_users': 0,
                'admin_users': 0,
                'new_users_this_week': 0,
                'verification_rate': 0
            }

    def get_recent_activity(self):
        """Get recent user registrations and activity"""
        try:
            recent_users = User.query.order_by(User.user_id.desc()).limit(5).all()
            activity = []
            for user in recent_users:
                activity.append({
                    'type': 'user_registered',
                    'message': f'New user: {user.name} ({user.email})',
                    'timestamp': getattr(user, 'created_at', 'Unknown'),
                    'status': 'verified' if user.is_verified else 'pending'
                })
            return activity
        except Exception:
            return []

class UserForm(BaseForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')  # For new users
    role = SelectField('Role', choices=[('visitor', 'Visitor'), ('admin', 'Admin')], default='visitor')
    is_verified = BooleanField('Is Verified', default=False)
    google_id = StringField('Google ID')
    profile_picture = StringField('Profile Picture URL')

class SecureModelView(ModelView):
    """Base class with authentication for all admin views"""
    def is_accessible(self):
        # TODO: Implement proper authentication check
        # return current_user.is_authenticated and current_user.role == 'admin'
        return True  # Temporarily allow all access for development

    def inaccessible_callback(self, name, **kwargs):
        # TODO: Redirect to login page
        # return redirect(url_for('auth.login'))
        return "Access Denied - Admin privileges required"

class UserModelView(SecureModelView):
    form = UserForm
    column_list = ['user_id', 'name', 'email', 'role', 'is_verified', 'created_at']
    column_exclude_list = ['password_hash']  # Hide sensitive data
    form_excluded_columns = ['password_hash', 'created_at', 'updated_at', 'last_login']

    # Add search functionality
    column_searchable_list = ['name', 'email']
    column_filters = ['role', 'is_verified']

    def on_model_change(self, form, model, is_created):
        # Hash password if provided
        if hasattr(form, 'password') and form.password.data:
            model.password_hash = generate_password_hash(form.password.data)

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    # Use custom dashboard as the home page
    admin = Admin(app,
                 name='Charity Directory Admin',
                 template_mode='bootstrap4',
                 index_view=DashboardView(name='Dashboard', template='admin/dashboard.html', url='/admin'))

    # Use secure model views with better validation
    admin.add_view(UserModelView(User, db.session, name='Users'))

    from .models import Organization, Category, Location, Notification, AuditLog, Advertisement

    # Apply security to all model views
    admin.add_view(SecureModelView(Organization, db.session, name='Organizations'))
    admin.add_view(SecureModelView(Category, db.session, name='Categories'))
    admin.add_view(SecureModelView(Location, db.session, name='Locations'))
    admin.add_view(SecureModelView(Notification, db.session, name='Notifications'))
    admin.add_view(SecureModelView(AuditLog, db.session, name='Audit Logs'))
    admin.add_view(SecureModelView(Advertisement, db.session, name='Advertisements'))
