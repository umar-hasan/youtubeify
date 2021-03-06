from . import db
from .playlists import Playlist
from .videos import Video

class PlaylistVideo(db.Model):
    __tablename__ = 'playlist_videos'

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    id = db.Column(db.Text, db.ForeignKey('videos.id'), nullable=False, primary_key=True)