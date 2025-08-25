from .db import db
from .models.user import User
from .models.organization import Organization
from .models.category import Category
from .models.location import Location
from .models.notification import Notification
from .models.audit_log import AuditLog
from .models.advertisement import Advertisement

# Register all models with SQLAlchemy
# (If using Flask-Migrate/Alembic, this ensures all models are detected)
