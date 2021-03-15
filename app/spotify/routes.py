from . import *
from .helpers import *
from ..models import db
from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_required

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

spot = Blueprint('spot', __name__, template_folder='../templates', static_folder='../static')


@spot.route("/spot-authorize")
@login_required
def spot_authorize():
    """Used to authenticate a user's Spotify account."""

    if request.referrer and url_for("api.settings", _external=True) in request.referrer:
      session["spot_referrer"] = request.referrer

    sp = create_spot_oauth_dialog()

    auth_url = sp.get_authorize_url()

    return redirect(auth_url)

@spot.route("/spot-oauth2callback")
@login_required
def spot_oauth2callback():
    """Redirect for the Spotify account login page."""

    sp = create_spot_oauth()

    credentials = sp.get_access_token(request.args.get("code"))
    
    user_creds = SpotCredentials.query.get(current_user.get_id())

    if not user_creds:
      user_creds = SpotCredentials(
        user_id=current_user.get_id(),
        token=credentials['access_token'],
        refresh_token=credentials['refresh_token'],
        expires_at=credentials['expires_in'])
      db.session.add(user_creds)
    else:
      user_creds.token = credentials['access_token']
      user_creds.refresh_token = credentials['refresh_token']
      user_creds.expires_at = credentials['expires_in']

    db.session.commit()

    if "custom_referrer" in session and session["custom_referrer"]:
      print(session["custom_referrer"])
      return redirect(session["custom_referrer"])

    if "spot_referrer" in session:
      flash("User update successful.", 'success')
      return redirect(session["spot_referrer"])

    return redirect(url_for("auth.verify"))


