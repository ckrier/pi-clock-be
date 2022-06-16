from os import environ
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# oauth configuration
SPOTIFY_CLIENT_ID = environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = environ['SPOTIFY_REDIRECT_URI']
SPOTIFY_AUTH_SCOPES = ['user-modify-playback-state', 'user-read-playback-state',
                       'playlist-read-collaborative', 'playlist-read-private']

# device id to be used for playback
SPOTIFY_DEVICE_ID = environ['SPOTIFY_DEVICE_ID']


def play():
    playlist_uri = 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp'

    client = __create_client__()

    client.shuffle(True, SPOTIFY_DEVICE_ID)
    client.start_playback(SPOTIFY_DEVICE_ID, playlist_uri)


def pause():
    client = __create_client__()
    client.pause_playback(SPOTIFY_DEVICE_ID)


def __create_client__():
    auth = SpotifyOAuth(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=','.join(SPOTIFY_AUTH_SCOPES)
    )

    return Spotify(auth_manager=auth)
