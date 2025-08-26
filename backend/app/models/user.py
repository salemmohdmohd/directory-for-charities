from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ..db import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255))
    role = Column(String(20), default='visitor')
    is_verified = Column(Boolean, default=False)
    google_id = Column(String(50))
    profile_picture = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_login = Column(DateTime)

    def __repr__(self):
        return f'<User {self.name}>'
