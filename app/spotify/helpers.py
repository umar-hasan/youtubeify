from . import *
from flask import render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_required, current_user
from ..models.spot_credentials import SpotCredentials
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials



def create_spot_playlist(name, description=""):
    """Creates a new Spotify playlist."""
    
    auth_manager = create_spot_oauth()

    sp = Spotify(auth_manager=auth_manager)

    return sp.user_playlist_create(user=sp.current_user()["id"], name=name, description=description)


def add_to_spot_playlist(playlist_id, tracks):
    """Adds a song to a Spotify playlist."""

    auth_manager = create_spot_oauth()

    sp = Spotify(auth_manager=auth_manager)

    return sp.user_playlist_add_tracks(user=sp.current_user()["id"], playlist_id=playlist_id, tracks=tracks)


def get_spot_credentials():
    """Gets user credentials for Spotify."""

    if not current_user.is_authenticated:
      return None

    user_creds = SpotCredentials.query.get(current_user.get_id())

    if not user_creds:
      return None

    sp = create_spot_oauth()

    token_info = {
      "access_token": user_creds.token,
      "refresh_token": user_creds.refresh_token,
      "scope": spot_scope
    }

    if 'spot_credentials' not in session:
      session['spot_credentials'] = token_info

    t = sp.validate_token(token_info)
    user_creds.token = t["access_token"]
    db.seesion.commit()

    return t


def create_spot_oauth():
    """Creates a SpotifyOAuth object."""

    return SpotifyOAuth(
        client_id=SPOT_CLIENT_ID, 
        client_secret=SPOT_CLIENT_SECRET, 
        redirect_uri=url_for("spot.spot_oauth2callback", _external=True),
        scope=spot_scope)


def spot_search_results(q):
    """Returns Spotify search results."""

    auth_manager = create_spot_oauth()

    sp = Spotify(auth_manager=auth_manager)

    res = sp.search(q=q, limit=50)

    return res


def spot_get_recommended():
    """Returns recommended Spotify songs based on a user's history."""

    auth_manager = create_spot_oauth()

    sp = Spotify(auth_manager=auth_manager)

    artist_seeds = [artist["external_urls"]["spotify"] for artist in sp.current_user_top_artists()["items"]]
    genre_seeds = sp.recommendation_genre_seeds()

    try:
      res = sp.recommendations(seed_artists=artist_seeds[:5], limit=10)
      return res["tracks"]
    except:
      return None
