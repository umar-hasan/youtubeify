from . import *
from flask import render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_required, current_user

from ..models.yt_credentials import YTCredentials

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 


def create_yt_playlist(name, description=""):
    """Creates a new YouTube playlist."""
    credentials = get_yt_credentials()
    if not credentials:
      return redirect(url_for('verify'))

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    req = youtube.playlists().insert(
          part="snippet",
          body={
            "snippet": {
              "title": name,
              "description": description
            }
          }
      )

    return req.execute()


def add_to_yt_playlist(playlist_id, video_id):
    """Adds a new video to a YouTube playlist."""

    credentials = get_yt_credentials()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    req = youtube.playlistItems().insert(
          part="snippet",
          body={
            "snippet": {
              "playlistId": playlist_id,
              "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
              }
            }
          }
        )

    req.execute()


def in_yt_playlist(video_id, playlist_id):
    """Checks if a video is in a YouTube playlist."""

    credentials = get_yt_credentials()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    req = youtube.playlistItems().list(
          part="snippet",
          maxResults=1,
          playlistId=playlist_id,
          videoId=video_id
      )
    res = req.execute()
    
    if video_id == res["items"][0]["snippet"]["resourceId"]["videoId"]:
      return True

    return False



def yt_credentials_to_dict(credentials):
    """Converts YouTube credentials to a dictionary."""

    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token}
            

def get_yt_credentials():
    """Gets the credentials for YouTube."""

    if not current_user.is_authenticated:
      return None

    user_creds = YTCredentials.query.get(current_user.get_id())

    if not user_creds:
      return None

    credentials = Credentials(
      token=user_creds.token,
      refresh_token=user_creds.refresh_token,
      token_uri=TOKEN_URI,
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      scopes=SCOPES
    )

    if not credentials.valid:
      return None
      
    if credentials.expired:
      credentials.refresh(Request())
      session['yt-credentials'] = yt_credentials_to_dict(credentials)
      user_creds.token = credentials.token
      user_creds.refresh_token = credentials.refresh_token
      db.session.commit()

    return credentials


def yt_search_results(q):
    """Returns YouTube search results."""

    credentials = get_yt_credentials()

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    req = youtube.search().list(
          part="snippet",
          q=q,
          maxResults=50,
          videoCategoryId="10",
          type="video"
      )

    try:
      res = req.execute()
      return res
    except HttpError as err:
      return None




def yt_trending_music():
    """Returns tranding YouTube music."""
    
    credentials = get_yt_credentials()

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    req = youtube.videos().list(
          part="snippet",
          chart="mostPopular",
          maxResults=10,
          videoCategoryId="10"
      )

    try:
      res = req.execute()
      return res
    except HttpError as err:
      return None