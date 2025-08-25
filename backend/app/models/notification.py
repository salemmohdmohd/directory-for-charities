from ..db import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    message = db.Column(db.String)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
