from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from .models import db
from .models.users import User
from .models.playlists import Playlist
from .models.videos import Video
from .models.songs import Song
from .models.playlist_videos import PlaylistVideo
from .models.playlist_songs import PlaylistSong
from .models.yt_credentials import YTCredentials
from .models.spot_credentials import SpotCredentials
from .ytube.helpers import *
from .spotify.helpers import *
from flask_login import login_required, current_user
from youtube_title_parse import get_artist_title
from .forms import ChangeUserForm, ChangePasswordForm


api = Blueprint('api', __name__, template_folder='./templates', static_folder='../static')



@api.route('/')
@login_required
def home():
    """Home page."""

    if "referrer" in session:
        session.pop("referrer")
        
    if not get_yt_credentials() or not get_spot_credentials():
      return redirect(url_for('auth.verify'))
    
    yt_trending = yt_trending_music()
    spot_recommended = spot_get_recommended()

    if not yt_trending:
      session["HttpError"] = "true"
      return redirect(url_for("auth.logout"))

    playlists = Playlist.query.filter_by(user_id=current_user.get_id())

    return render_template('home.html', 
                            yt_trending=yt_trending["items"], 
                            spot_recommended=spot_recommended["tracks"],
                            playlists=playlists)


@api.route("/settings")
@login_required
def settings():
    """Settings page."""

    if "referrer" in session:
        session.pop("referrer")

    if "yt_referrer" in session:
        session.pop("yt_referrer")

    if "spot_referrer" in session:
        session.pop("spot_referrer")


    if not get_yt_credentials() or not get_spot_credentials():
      return redirect(url_for('auth.verify'))

    user_form = ChangeUserForm()
    password_form = ChangePasswordForm()

    user_form.username.data = current_user.username

    return render_template("settings.html", user_form=user_form, password_form=password_form)


@api.route("/change-username", methods=['POST'])
def change_username():
    """Handles changing username."""

    user_form = ChangeUserForm()
    password_form = ChangePasswordForm()

    if user_form.validate_on_submit():
      try:
        user = User.authenticate(username=current_user.username, password=user_form.password.data)
        if not user:
          flash("Invalid password.", 'password_error')
          return redirect(url_for("api.settings"))
        if user_form.username.data != current_user.username and len(user_form.username.data) > 0:
          updated_user = User.change_credentials(username=current_user.username, 
                                                 new_username=user_form.username.data)
          flash("User update successful.", 'success')

      except:
        flash("User update failed.", 'error')
      
    
    return redirect(url_for("api.settings"))


@api.route("/change-pass", methods=['POST'])
def change_pass():
    """Handles changing user's password."""

    user_form = ChangeUserForm()
    password_form = ChangePasswordForm()

    if password_form.validate_on_submit():
      try:
        user = User.authenticate(username=current_user.username, password=password_form.current_password.data)
        if not user:
          flash("Invalid password.", 'current_password_error')
          return redirect(url_for("api.settings"))
        if len(password_form.new_password.data) < 8 or len(password_form.new_password.data) > 30:
          flash("Password must be between 8 and 30 characters.", 'new_password_error')
          return redirect(url_for("api.settings"))
        if password_form.confirm_new_password.data != password_form.new_password.data:
          flash("Passwords must match.", 'confirm_new_password_error')
          return redirect(url_for("api.settings"))
        
        
        updated_user = User.change_credentials(username=current_user.username, 
                                              password=password_form.new_password.data)
        flash("User update successful.", 'success')

      except:
        flash("User update failed.", 'error')
    
    return redirect(url_for("api.settings"))


@api.route("/search-results")
@login_required
def search_results():
    """Displays search results based on a user's query."""

    if "referrer" in session:
        session.pop("referrer")
    if not get_yt_credentials() or not get_spot_credentials():
      return redirect(url_for('auth.verify'))
    q = " "
    if request.args.get("query"):
      q = request.args.get("query")
    yt_results = yt_search_results(q)
    spot_results = spot_search_results(q)

    if not yt_results:
      session["HttpError"] = "true"
      return redirect(url_for("auth.logout"))

    playlists = Playlist.query.filter_by(user_id=current_user.get_id())

    return render_template("search_results.html", 
                            yt_results=yt_results["items"], 
                            spot_results=spot_results["tracks"]["items"],
                            playlists=playlists)


@api.route("/playlists")
@login_required
def show_playlists():
    """Shows playlists a user has created."""

    if "referrer" in session:
        session.pop("referrer")
    if not get_yt_credentials() or not get_spot_credentials():
      return redirect(url_for('auth.verify'))
    user = User.query.get(current_user.get_id())
    playlists = user.playlists

    info = []
    for p in playlists:
      if p.videos:
        img = Video.query.get(p.videos[0].id).img_url
        info.append({"playlist": p, "img": img})
      elif p.songs:
        img = Song.query.get(p.songs[0].id).img_url
        info.append({"playlist": p, "img": img})
      else:
        info.append({"playlist": p})

    return render_template("playlists.html", playlists=info)


@api.route("/create-playlist", methods=['POST'])
def create_playlist():
    """Creates a new playlist."""

    data = request.get_json()
    playlist = Playlist(
      user_id=current_user.get_id(),
      name=data["name"],
      description=data["description"]
    )
    db.session.add(playlist)
    db.session.commit()
    db.session.refresh(playlist)
    
    return f"{playlist.id}"


@api.route("/update-playlist", methods=['POST'])
def upate_playlist():
    """Updates the playlist title/description."""
    data = request.get_json()
    playlist = Playlist.query.get(data["id"])
    playlist.name = data["name"]
    playlist.description = data["description"]
    db.session.commit()
    
    return f"{playlist.id}"


@api.route("/delete-playlist", methods=['POST'])
def delete_playlist():
    """Deletes a playlist a user has created."""

    playlist = Playlist.query.get(int(request.form["playlist_id"]))
    if playlist.videos:
      for video in playlist.videos:
        remove_content(video.id, video=video)
    if playlist.songs:
      for song in playlist.songs:
        remove_content(song.id, song=song)
    db.session.delete(playlist)
    db.session.commit()
    flash("Playlist successfully deleted.", 'success')
    return redirect(url_for("api.show_playlists"))


@api.route("/playlist/<int:id>")
def view_playlist(id):
    """Shows all the music and videos in a specific playlist."""

    playlist = Playlist.query.get(id)
    if not playlist or playlist.user_id is not int(current_user.get_id()):
      return redirect(request.referrer)

    videos = []
    songs = []

    for video in playlist.videos:
      v = Video.query.get(video.id)
      videos.append(v)

    for song in playlist.songs:
      s = Song.query.get(song.id)
      songs.append(s)

    return render_template("playlist.html", playlist=playlist, videos=videos, songs=songs)


@api.route("/add", methods=['POST'])
def add_to_playlists():
    """Adds a song or video to one or more playlists."""

    data = request.get_json()
    playlists = data["playlists"]

    for pid in playlists:
      p = Playlist.query.get(pid)
      if data["type"] == "video":
        if not Video.query.get(data["content"]["id"]):
          video = Video(
            id=data["content"]["id"],
            img_url=data["content"]["img"],
            title=data["content"]["title"],
            channel=data["content"]["channel"]
          )
          db.session.add(video)
          db.session.commit()
        try:
          v = PlaylistVideo(
            playlist_id=pid,
            id=data["content"]["id"]
          )
          db.session.add(v)
          db.session.commit()
        except:
          db.session.rollback()
      elif data["type"] == "song":
        if not Song.query.get(data["content"]["id"]):
          song = Song(
            id=data["content"]["id"],
            img_url=data["content"]["img"],
            title=data["content"]["title"],
            artist=data["content"]["artist"]
          )
          db.session.add(song)
          db.session.commit()
        try:
          s = PlaylistSong(
            playlist_id=pid,
            id=data["content"]["id"]
          )
          db.session.add(s)
          db.session.commit()
        except:
          db.session.rollback()

    return "success"


@api.route("/remove", methods=['POST'])
def remove_from_playlist():
    """Deletes a song or video from a playlist."""

    data = request.get_json()
    if data["type"] == "video":
      pv = PlaylistVideo.query.filter_by(playlist_id=int(data["playlistId"]), id=data["id"]).first()
      remove_content(data["id"], video=pv)
    elif data["type"] == "song":
      ps = PlaylistSong.query.filter_by(playlist_id=int(data["playlistId"]), id=data["id"]).first()
      remove_content(data["id"], song=ps)
    
    return "success"


def remove_content(id, video=None, song=None):
    """Helper for removing a song or video from a playlist."""
    if video:
      db.session.delete(video)
      db.session.commit()
      if not PlaylistVideo.query.filter_by(id=id).first():
        v = Video.query.get(id)
        db.session.delete(v)
        db.session.commit()

    elif song:
      db.session.delete(song)
      db.session.commit()
      if not PlaylistSong.query.filter_by(id=id).first():
        s = Song.query.get(id)
        db.session.delete(s)
        db.session.commit()


@api.route("/yt-export", methods=['POST'])
def export_to_yt():
    """Exports a playlist to YouTube."""
    
    if not get_yt_credentials() or not get_spot_credentials():
      return redirect(url_for('auth.verify'))
    
    try:
      playlist = Playlist.query.get(int(request.form["playlist_id"]))

      yt_playlist = create_yt_playlist(playlist.name, playlist.description)
      yt_playlist_id = yt_playlist["id"]


      if playlist.videos:
        for video in playlist.videos:
          add_to_yt_playlist(yt_playlist_id, video.id)
          remove_content(video.id, video=video)
      

      if playlist.songs:
        for song in playlist.songs:
          s = Song.query.get(song.id)
          query = s.title + " " + s.artist
          video_results = yt_search_results(query)["items"]
          for result in video_results:
            if s.title in result["snippet"]["title"] or s.artist in result["snippet"]["channelTitle"] or s.artist.strip() in result["snippet"]["channelTitle"] or s.artist in result["snippet"]["title"]:
              if in_yt_playlist(result["id"]["videoId"], yt_playlist_id):
                continue
              add_to_yt_playlist(yt_playlist_id, result["id"]["videoId"])
              break
          remove_content(song.id, song=song)

      db.session.delete(playlist)
      db.session.commit()

      flash("Playlist successfully exported to YouTube.", 'success')

    except Exception as e:
      print(e)
      flash("Unable to export playlist to YouTube.", 'error')
    
    return redirect(url_for("api.show_playlists"))


@api.route("/spot-export", methods=['POST'])
def export_to_spot():
    """Exports a playlist to Spotify."""

    if not get_yt_credentials() or not get_spot_credentials():
      return redirect(url_for('auth.verify'))

    try:
      playlist = Playlist.query.get(int(request.form["playlist_id"]))

      spot_playlist = create_spot_playlist(playlist.name, description=playlist.description)
      spot_playlist_id = spot_playlist["id"]


      if playlist.songs:
        tracks = [s.id for s in playlist.songs]
        
        add_to_spot_playlist(spot_playlist_id, tracks)

        for song in playlist.songs:
          remove_content(song.id, song=song)

      

      tracks = []
      if playlist.videos:
        for video in playlist.videos:
          v = Video.query.get(video.id)
          query = v.title
          start = query.find("[")
          end = query.find("]")
          if start != -1 and end != -1:
            query = query.replace(query[query.find("["):query.find("]")+1], "")
          query = query.replace(query[query.find("("):query.find(")")+1], "")
          query = query.replace("by", "")

          q1 = None
          q2 = None

          if get_artist_title(query):
            q1, q2 = get_artist_title(query)
            q1 = q1.replace(")", "")
            q1 = q1.replace("(", "")
            q1 = q1.replace("[", "")
            q1 = q1.replace("]", "")
            q2 = q2.replace(")", "")
            q2 = q2.replace("(", "")
            q2 = q2.replace("[", "")
            q2 = q2.replace("]", "")

          print(query)
          print(q1)
          print(q2)


          if q1 and q2:
            song_results = spot_search_results(q1)["tracks"]["items"]
            if song_results:
              for result in song_results:
                
                if (result["name"].lower() in v.title.lower() and result["artists"][0]["name"] in v.title) or (result["name"].replace(result["name"][result["name"].find("["):result["name"].find("]")+1], "").lower() in v.title.lower() and result["artists"][0]["name"] in v.title):
                  if result["id"] in tracks:
                    continue
                  else:
                    tracks.append(result["id"])
                    break
            
            if not song_results or not tracks:
              song_results = spot_search_results(q2)["tracks"]["items"]
              if song_results:
                for result in song_results:
                  if (result["name"].lower() in v.title.lower() and result["artists"][0]["name"] in v.title) or (result["name"].replace(result["name"][result["name"].find("["):result["name"].find("]")+1], "").lower() in v.title.lower() and result["artists"][0]["name"] in v.title):
                    if result["id"] in tracks:
                      continue
                    else:
                      tracks.append(result["id"])
                      break
          else:
            song_results = spot_search_results(query)["tracks"]["items"]
            if song_results:
              for result in song_results:
                 if (result["name"].lower() in v.title.lower() and result["artists"][0]["name"] in v.title) or (result["name"].replace(result["name"][result["name"].find("["):result["name"].find("]")+1], "").lower() in v.title.lower() and result["artists"][0]["name"] in v.title):
                  if result["id"] in tracks:
                      continue
                  else:
                    tracks.append(result["id"])
                    break
              
          remove_content(video.id, video=video)


      if tracks:
        add_to_spot_playlist(spot_playlist_id, tracks)

      db.session.delete(playlist)
      db.session.commit()
      
      flash("Playlist successfully exported to Spotify.", 'success')

    except Exception as e:
      flash("Unable to export playlist to Spotify.", 'error')
      
    
    return redirect(url_for("api.show_playlists"))