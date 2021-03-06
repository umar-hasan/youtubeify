from . import db
from .users import User

class YTCredentials(db.Model):
    __tablename__ = 'yt_credentials'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)