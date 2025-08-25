from ..db import db

class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    ad_id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.org_id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    target_url = db.Column(db.String(500))
    ad_type = db.Column(db.String(50), nullable=False)
    placement = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Numeric(10,2))
    clicks_count = db.Column(db.Integer, default=0)
    impressions_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
