import os
import unittest
import flask_unittest
from flask_unittest import ClientTestCase
from app import app
from flask import Blueprint, render_template, redirect, request, url_for, session, jsonify, flash
from app.models import db 
from app.models.users import User
from app.models.spot_credentials import SpotCredentials 
from app.models.yt_credentials import YTCredentials
from flask_login import current_user

class TestApi(ClientTestCase):

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
                res = client.post(url_for('auth.register'), data={'username': 'test', 'password': 'password', 'confirm_password': 'password'})

    def tearDown(self, client):
        with app.app_context():
            db.drop_all()


    def test_1_register(self, client):
        """Registers a new user."""

        with app.app_context():
            res = client.post(url_for('auth.register'), data={'username': 'test2', 'password': 'password', 'confirm_password': 'password'})
            user = User.query.filter_by(username='test').first()
            self.assertEqual(res.status_code, 302)
            self.assertNotEqual(user, None)



    def test_2_login(self, client):
        """Logs a user into the app."""

        with app.app_context():
            res = client.post(url_for('auth.login'), data={'username': 'test', 'password': 'password'})
            self.assertLocationHeader(res, 'http://localhost.com:5000' + url_for('api.home'))


    def test_3_delete_user(self, client):
        """Deletes a user account entirely."""

        with app.app_context():
            client.post(url_for('auth.login'), data={'username': 'test', 'password': 'password'})

            yt_creds = YTCredentials(
                user_id=current_user.get_id(),
                token="ABCDEF",
                refresh_token="GHIJKL")
            db.session.add(yt_creds)
            db.session.commit()

            spot_creds = SpotCredentials(
                user_id=current_user.get_id(),
                token="ABCDEF",
                refresh_token="GHIJKL")
            db.session.add(spot_creds)
            db.session.commit()

            res = client.post(url_for('auth.delete_user'))

            user = User.query.filter_by(username='test').first()
            self.assertEqual(user, None)
        

