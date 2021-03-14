# You'll need to have your own Spotify API credentials for this part.
import os

SPOT_CLIENT_ID = os.environ.get('SPOT_CLIENT_ID')
SPOT_CLIENT_SECRET = os.environ.get('SPOT_CLIENT_SECRET')

spot_scope = "playlist-modify-public user-top-read"