from . import db

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Text, nullable=False, primary_key=True)
    img_url = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    channel = db.Column(db.Text, nullable=False)