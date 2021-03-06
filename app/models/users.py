from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from . import db

bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    playlists = db.relationship('Playlist')

    @classmethod
    def signup(cls, username, password, confirm_pwd):
        if password != confirm_pwd:
            return False

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        return user

    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    
    @classmethod
    def change_credentials(cls, username, new_username=None, password=None):

        user = cls.query.filter_by(username=username).first()

        if new_username:
            existing_user = cls.query.filter_by(username=new_username).first()
            if existing_user:
                return None

        if user:
            if password:
                hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
                user.password = hashed_pwd
            if new_username:
                user.username = new_username
            db.session.commit()
            return user

        return "There was an issue updating the user."