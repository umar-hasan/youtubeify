from . import db
from .users import User

class SpotCredentials(db.Model):
    __tablename__ = 'spot_credentials'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    expires_at = db.Column(db.Text)