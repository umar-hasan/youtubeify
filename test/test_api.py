import unittest
from unittest.mock import patch, Mock
from unittest import TestCase
import json
from app import app
from app.models import db 
from app.ytube.helpers import *
from app.spotify.helpers import *
from spotipy import Spotify
from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import current_user

from parameters import *

class TestApi(TestCase):

    app = app
    db.init_app(app)

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["SERVER_NAME"] = 'localhost.com:5000'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///youtubeify_test'
        
        with app.app_context():
            with app.test_client() as client:
                db.create_all()
                client.post(url_for('auth.register'), data={'username': 'test', 'password': 'password', 'confirm_password': 'password'})
                

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    @patch('app.ytube.helpers.get_yt_credentials')
    @patch('app.ytube.helpers.build')
    @patch('app.spotify.helpers.get_spot_credentials')
    @patch.object(Spotify, "search")
    def test_search_results(self, mock_spot_search, mock_spot_cred, mock_yt_search, mock_yt_cred):
        """Tests to see if the search functionality works on both YouTube and Spotify."""
        
        mock_yt_search.return_value.search.return_value.list.return_value.execute.return_value = YT_SEARCH_TEST
        mock_spot_search.return_value = SPOT_SEARCH_TEST
        yt_search = yt_search_results("iridescent")
        spot_search = spot_search_results("iridescent")

        mock_yt_search.assert_called_once()
        mock_spot_search.assert_called_once()
        
        self.assertEqual(len(yt_search["items"]), 5)
        self.assertEqual(len(spot_search["tracks"]["items"]), 2)


