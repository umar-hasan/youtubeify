# You'll need to have your own YouTube API credentials for this part.

import os

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

CLIENT_ID = os.environ.get('CLIENT_ID')
PROJECT_ID = os.environ.get('PROJECT_ID')
AUTH_URI = os.environ.get('AUTH_URI')
TOKEN_URI = os.environ.get('TOKEN_URI')
AUTH_PROVIDER_URL = os.environ.get('AUTH_PROVIDER_URL')
CLIENT_SECRET = os.environ('CLIENT_SECRET')
REDIRECT_URIS = os.environ.get('REDIRECT_URIS')

CLIENT_CONFIG = {
    "web": {
        "client_id": CLIENT_ID,
        "project_id": PROJECT_ID,
        "auth_uri": AUTH_URI,
        "token_uri": TOKEN_URI,
        "auth_provider_x509_cert_url": AUTH_PROVIDER_URL,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": REDIRECT_URIS
    }
}
SCOPES = ['https://www.googleapis.com/auth/youtube']