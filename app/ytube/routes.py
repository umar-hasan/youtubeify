from . import *
from .helpers import *
from ..models import db
from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_required, current_user

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 

yt = Blueprint('yt', __name__, template_folder='../templates', static_folder='../static')


@yt.route("/yt-authorize")
@login_required
def yt_authorize():
    """Used to authenticate a user's YouTube account."""

    if request.referrer and url_for("api.settings", _external=True) in request.referrer:
      session["yt_referrer"] = request.referrer

    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES
    )

    flow.redirect_uri = url_for('yt.yt_oauth2callback', _external=True)

    auth_url, state = flow.authorization_url()

    session["yt_state"] = state

    return redirect(auth_url)


@yt.route('/yt_oauth2callback')
@login_required
def yt_oauth2callback():
    """Redirect for the YouTube login page."""

    state = session['yt_state']

    flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('yt.yt_oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    user_creds = YTCredentials.query.get(current_user.get_id())
    if not user_creds:
      user_creds = YTCredentials(
        user_id=current_user.get_id(),
        token=credentials.token,
        refresh_token=credentials.refresh_token)
      db.session.add(user_creds)
    else:
      user_creds.token = credentials.token
      if credentials.refresh_token:
        user_creds.refresh_token = credentials.refresh_token

    db.session.commit()


    del session['yt_state']

    if "custom_referrer" in session and session["custom_referrer"]:
      return redirect(session["custom_referrer"])

    if "yt_referrer" in session:
      flash("User update successful.", 'success')
      return redirect(session["yt_referrer"])

    return redirect(url_for("auth.verify"))

