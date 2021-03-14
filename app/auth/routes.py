from . import login_manager
from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..models import db
from ..models.users import User
from ..models.playlists import Playlist
from ..models.videos import Video
from ..models.songs import Song
from ..models.playlist_videos import PlaylistVideo
from ..models.playlist_songs import PlaylistSong
from ..models.yt_credentials import YTCredentials
from ..models.spot_credentials import SpotCredentials
from ..forms import LoginForm, RegisterForm
from ..routes import remove_content
from ..ytube.helpers import get_yt_credentials
from ..spotify.helpers import get_spot_credentials

auth = Blueprint('auth', __name__, template_folder='../templates', static_folder='../static')


def page_not_found(e):
    """Shows a custom 404 page."""

    return render_template("error.html"), 404

@auth.route("/verify")
@login_required
def verify():
    """Verification page leading to YouTube and Spotify account login pages."""

    session["referrer"] = request.referrer
    yt_verified = False
    spot_verified = False
    if get_yt_credentials():
      yt_verified = True
    if get_spot_credentials():
      spot_verified = True

    return render_template('verify.html', yt_verified=yt_verified, spot_verified=spot_verified)

@login_manager.user_loader
def load_user(user_id):
    """Loads a user when logging in."""

    return User.query.get(user_id)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    """Logs the user into the application."""

    if current_user.is_authenticated:
      return redirect(url_for('api.home'))
    form = LoginForm()
    if form.validate_on_submit():
      user = User.authenticate(username=form.username.data, password=form.password.data)
      if not user:
        flash('Invalid username/password.', 'error')
      else:
        login_user(user)
        return redirect(url_for('api.home'))

    return render_template("login.html", form=form)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    """Registers a new user."""

    if current_user.is_authenticated:
      return redirect(url_for('api.home'))
    form = RegisterForm()
    if form.validate_on_submit():
      user = User.signup(username=form.username.data, password=form.password.data, confirm_pwd=form.confirm_password.data)
      try:
        db.session.add(user)
        db.session.commit()
        flash('User creation successful. You should be able to login.', 'success')
        return redirect(url_for('auth.login'))
      except:
        if not user:
          flash('Password not confirmed.', 'error')
        else:
          flash('Username already exists!', 'error')

    return render_template("register.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """Logs a user out."""
    
    errors = False
    if "HttpError" in session:
      errors = True
    logout_user()
    session.clear()
    if errors:
      flash("Looks like YouTube's quota limit has been broken. You have been logged out. Please try again later.", 'error')
    else:
      flash("Logout successful.", 'success')
    return redirect(url_for('auth.login'))


@auth.route("/delete-user", methods=['POST'])
@login_required
def delete_user():
    """Deletes a user account and information."""

    user = User.query.get(current_user.get_id())
    playlists = Playlist.query.filter_by(user_id=current_user.get_id()).all()
    for playlist in playlists:
      for v in playlist.videos:
        remove_content(v.id, video=v)
      for s in playlist.songs:
        remove_content(s.id, song=s)
      db.session.delete(playlist)
      db.session.commit()

    

    yt = YTCredentials.query.get(current_user.get_id())
    spot = SpotCredentials.query.get(current_user.get_id())

    logout_user()
    session.clear()
    
    db.session.delete(yt)
    db.session.commit()
    db.session.delete(spot)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()

    flash("Account has been successfully deleted.", 'success')
    return redirect(url_for("auth.login"))
