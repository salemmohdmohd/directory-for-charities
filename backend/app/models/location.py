from ..db import db

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    state_province = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20))
    latitude = db.Column(db.Numeric(10,8))
    longitude = db.Column(db.Numeric(11,8))
    timezone = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
