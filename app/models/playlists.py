from . import db
from .users import User

class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text)
    description = db.Column(db.Text, default="")

    videos = db.relationship('PlaylistVideo')
    songs = db.relationship('PlaylistSong')