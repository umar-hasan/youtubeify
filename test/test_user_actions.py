import os
import unittest
import flask_unittest
from flask_unittest import ClientTestCase
from app import app
from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from app.models import db 
from app.models.users import User
from app.models.playlists import Playlist
from app.models.videos import Video
from app.models.songs import Song
from app.models.playlist_videos import PlaylistVideo
from app.models.playlist_songs import PlaylistSong

from flask_login import current_user


class TestUserActions(ClientTestCase):

    app = app
    db.init_app(app)

    def setUp(self, client):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["SERVER_NAME"] = 'localhost.com:5000'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///youtubeify_test'
        with app.app_context():
            with app.test_client() as client:
                db.create_all()
                client.post(url_for('auth.register'), data={'username': 'test', 'password': 'password', 'confirm_password': 'password'})
                client.post(url_for('auth.login'), data={'username': 'test', 'password': 'password'})

    def tearDown(self, client):
        with app.app_context():
            db.drop_all()



    def test_1_create_playlist(self, client):
        """Creates a playlist."""

        with app.app_context():
            res = client.post(url_for('api.create_playlist'), json={
                'name': 'Test Playlist', 
                'description': 'This is a test playlist.'})

            playlist = Playlist.query.get(1)
            self.assertNotEqual(playlist, None)

        
    def test_2_add_video_to_playlist(self, client):
        """Adds a YouTube video to a playlist."""

        with app.app_context():
            client.post(url_for('api.create_playlist'), json={
                'name': 'Test Playlist', 
                'description': 'This is a test playlist.'})
            res = client.post(url_for('api.add_to_playlists'), json={
                'content': {
                    'id': 'asdf',
                    'img': '',
                    'title': '',
                    'channel': ''
                },
                'playlists': ['1'], 
                'type': 'video'})

            playlist = Playlist.query.get(1)

            self.assertEqual(len(playlist.videos), 1)

            


    def test_3_add_song_to_playlist(self, client):
        """Adds a Spotify song to a playlist."""

        with app.app_context():
            client.post(url_for('api.create_playlist'), json={
                'name': 'Test Playlist', 
                'description': 'This is a test playlist.'})
            res = client.post(url_for('api.add_to_playlists'), json={
                'content': {
                    'id': 'qwerty',
                    'img': '',
                    'title': '',
                    'artist': ''
                },
                'playlists': ['1'], 
                'type': 'song'})

            playlist = Playlist.query.get(1)

            self.assertEqual(len(playlist.songs), 1)



    def test_4_remove_video(self, client):
        """Removes a video from a playlist."""

        with app.app_context():
            client.post(url_for('api.create_playlist'), json={
                'name': 'Test Playlist', 
                'description': 'This is a test playlist.'})
            client.post(url_for('api.add_to_playlists'), json={
                'content': {
                    'id': 'asdf',
                    'img': '',
                    'title': '',
                    'channel': ''
                },
                'playlists': ['1'], 
                'type': 'video'})
            res = client.post(url_for('api.remove_from_playlist'), json={
                'playlistId': "1",
                'id': "asdf",
                'type': 'video'})

            playlist = Playlist.query.get(1)

            self.assertEqual(len(playlist.videos), 0)



    def test_5_remove_song(self, client):
        """Removes a song from a playlist."""

        with app.app_context():
            client.post(url_for('api.create_playlist'), json={
                'name': 'Test Playlist', 
                'description': 'This is a test playlist.'})
            client.post(url_for('api.add_to_playlists'), json={
                'content': {
                    'id': 'qwerty',
                    'img': '',
                    'title': '',
                    'channel': ''
                },
                'playlists': ['1'], 
                'type': 'video'})
            res = client.post(url_for('api.remove_from_playlist'), json={
                'playlistId': "1",
                'id': "qwerty",
                'type': 'song'})
            
            playlist = Playlist.query.get(1)

            self.assertEqual(len(playlist.songs), 0)



    def test_6_delete_playlist(self, client):
        """Deletes a playlist."""

        with app.app_context():
            client.post(url_for('api.create_playlist'), json={
                'name': 'Test Playlist', 
                'description': 'This is a test playlist.'})
            res = client.post(url_for("api.delete_playlist"), data={
                'playlist_id': '1'
            })

            playlist = Playlist.query.get(1)

            self.assertIsNone(playlist)