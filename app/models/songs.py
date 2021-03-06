from . import db

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Text, nullable=False, primary_key=True)
    img_url = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)