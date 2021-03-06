from . import db
from .playlists import Playlist
from .songs import Song

class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    id = db.Column(db.Text, db.ForeignKey('songs.id'), nullable=False, primary_key=True)