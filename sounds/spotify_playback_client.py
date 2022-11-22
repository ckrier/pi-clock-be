from os import environ
import socket

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# ip to redirect to on the fe
MACHINE_IP = environ['MACHINE_IP']

# oauth configuration
SPOTIFY_CLIENT_ID = environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = environ['SPOTIFY_REDIRECT_URI']
SPOTIFY_AUTH_SCOPES = ['user-modify-playback-state', 'user-read-playback-state',
                       'playlist-read-collaborative', 'playlist-read-private']

# device id to be used for playback
SPOTIFY_DEVICE_ID = environ['SPOTIFY_DEVICE_ID']

_auth_manager = SpotifyOAuth(
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=','.join(SPOTIFY_AUTH_SCOPES),
    show_dialog=True
)

_spotify_client = Spotify(auth_manager=_auth_manager)


def login(code):
    if code is not None:
        # Step 2. Being redirected from Spotify auth page
        _auth_manager.get_access_token(code)
        return f'http://{MACHINE_IP}:3000/settings'

    if not _auth_manager.validate_token(_auth_manager.cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        return _auth_manager.get_authorize_url()

    return f'http://{MACHINE_IP}:3000/settings'


def play():
    playlist_uri = 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp'

    client = _spotify_client

    client.shuffle(True, SPOTIFY_DEVICE_ID)
    client.start_playback(SPOTIFY_DEVICE_ID, playlist_uri)


def pause():
    client = _spotify_client

    if (is_playing(client)):
        client.pause_playback(SPOTIFY_DEVICE_ID)


def is_playing(client):
    if (client is None):
        client = _spotify_client

    playback = client.current_playback()
    return (playback is not None
            and playback['is_playing']
            and playback['device']['id'] == SPOTIFY_DEVICE_ID)
