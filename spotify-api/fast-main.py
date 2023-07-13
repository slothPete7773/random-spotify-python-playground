import time
import configparser
config = configparser.ConfigParser()
config.read("env.conf")

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
app = FastAPI()

CLIENT_ID=config.get('spotify_credential', 'CLIENT_ID')
CLIENT_SECRET=config.get('spotify_credential', 'CLIENT_SECRET')
REDIRECT_URI="http://localhost:8000/authorization"
# A list of space-separated scopes
SCOPE = "user-read-playback-state"

# Route methods
@app.get("/")
async def _root(token: str=None):
    _token, is_token_valid = get_access_token()
    _expires_at, is_expires_valid = get_expires_at()
    return {
        "greet": "Hello World",
        "page": "/",
        "access_token": _token if is_token_valid else "Empty",
        "expires_at": _expires_at if is_expires_valid else "Empty",
        }

@app.get("/login")
async def _login() -> RedirectResponse:
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(f"Authen URL: [{auth_url}]")
    return RedirectResponse(url=auth_url)
    
@app.get("/authorization")
async def _authorization(code: str=None):
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.get_access_token(code)

    if not (config.has_section("token_info")):
        config.add_section("token_info")    
    config.set("token_info", "access_token", token_info['access_token'])
    config.set("token_info", "token_type", token_info['token_type'])
    config.set("token_info", "expires_in", str(token_info['expires_in']))
    config.set("token_info", "scope", token_info['scope'])
    config.set("token_info", "expires_at", str(token_info['expires_at']))
    config.set("token_info", "refresh_token", token_info['refresh_token'])
    with open('env.conf', 'w') as config_file:
        config.write(config_file)
    
    return RedirectResponse(url=f"/?token={token_info}")

@app.get("/spotify-api/v1/me")
async def _me():
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    result = sp.current_user()
    return result

@app.get("/spotify-api/v1/me/top/{type}")
async def _top(type: str, time_range: int = 'medium_term', limit: int = 20, offset: int = 0):
    time_ranges = ['short_term', 'medium_term', 'long_term']
    valid_types = ['artists', 'tracks']
    if not (type in valid_types):
        raise HTTPException(status_code=404, detail='Invalid path parameter')

    if not (time_range in time_ranges):
        raise HTTPException(status_code=400, detail='Invalid provided time_range.')
    
    if not (limit >= 0 and limit <= 50):
        raise HTTPException(status_code=400, detail='Invalid range of value limit.')

    if (offset < 0):
        raise HTTPException(status_code=400, detail='Offset cannot less than 0.')
    
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    if (type == 'artists'):
        result = sp.current_user_top_artists(limit=limit, offset=offset, time_range=time_range)
    else:
        result = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)
    
    return result

class Artists(BaseModel):
    ids: list[str]

# EXAMPLE_IDS = ["4YPiq62lEVjRdzhSlNto08", "4YLUMAgNyttwx4hUHgtBtR"]
@app.post("/spotify-api/v1/artists")
async def _artists(artists: Artists):
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    result = sp.artists(artists.ids)
    return result

class Tracks(BaseModel):
    ids: list[str]

# EXAMPLE_IDS = ["5nDIBUarJMA7qlpuiryATA", "1enL3bmUAoP3sE1jp7NGP5"]
@app.post("/spotify-api/v1/tracks")
async def _tracks(tracks: Tracks):
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    result = sp.tracks(tracks.ids)
    return result

class Albums(BaseModel):
    ids: list[str]

# EXAMPLE_IDS = ["29vqF5DQuNIzcYM0tept6C", "20hW2P3VSNJ1A7MwjIJ0Up"]
@app.post("/spotify-api/v1/albums")
async def _albums(albums: Albums):
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    result = sp.albums(albums.ids)
    return result

@app.post("/spotify-api/v1/albums/genres")
async def _albums_genre(albums: Albums):
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    fetched_albums = sp.albums(albums.ids)
    albums_genre = []
    for album in fetched_albums['albums']:
        _temp = {
            "album_id" : album['id'],
            "album_name" : album['name'],
            "album_genre" : album['genres'] if len(album['genres']) > 0 else None
            }
        albums_genre.append(_temp)
    
    return {
        "albums_genre": albums_genre
    }

@app.post("/spotify-api/v1/artists/genres")
async def _artists_genre(artists: Artists):
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    fetched_artists = sp.artists(artists.ids)
    artists_genre = []
    for artist in fetched_artists['artists']:
        _temp = {
            "artist_id": artist['id'],
            "artist_name": artist['name'],
            "artist_genres": artist['genres']
        }
        artists_genre.append(_temp)
    
    return {
        "artists_genre": artists_genre
    }

@app.get("/spotify-api/v1/me/current_playback")
async def _current_playback():
    """
    Note: The result
    """
    token, is_authorized = get_access_token()
    if not(is_authorized):
        return RedirectResponse(url="/")
    
    sp = spotipy.Spotify(auth=token)
    current_playback = sp.current_playback()
    
    return current_playback
    

# Utility functions
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE 
    )

def get_access_token() -> tuple[str, bool]:
    token, is_token_valid = get_token_info()
    return token['access_token'], is_token_valid

def get_expires_at() -> tuple[int, bool]:
    token, is_token_valid = get_token_info()
    return token['expires_at'], is_token_valid

def get_token_info() -> tuple[dict, bool]:
    sp_oauth = create_spotify_oauth()
    token_info = {}
    is_token_valid = False
    # If token is not cached, return false
    if not (config.has_section("token_info")):
        is_token_valid = False
        return token_info, is_token_valid
    
    # Check if the token has expired
    now = int(time.time())
    is_token_expired = int(config.get('token_info', 'expires_at')) - now < 60

    if (is_token_expired):
        print('token is expired')
        refresh_token = config.get('token_info', 'refresh_token')
        token_info = sp_oauth.refresh_access_token(refresh_token)
        config.set("token_info", "access_token", token_info['access_token'])
        config.set("token_info", "token_type", token_info['token_type'])
        config.set("token_info", "expires_in", str(token_info['expires_in']))
        config.set("token_info", "scope", token_info['scope'])
        config.set("token_info", "expires_at", str(token_info['expires_at']))
        config.set("token_info", "refresh_token", token_info['refresh_token'])

    scope = config.get("token_info", "scope")
    token_type = config.get("token_info", "token_type")
    expires_in = config.get("token_info", "expires_in")
    expires_at = config.get("token_info", "expires_at")
    access_token = config.get("token_info", "access_token")
    refresh_token = config.get("token_info", "refresh_token")

    output = {
        "access_token": access_token,
        "token_type": token_type,
        "expires_in": expires_in,
        "scope": scope,
        "expires_at": expires_at,
        "refresh_token": refresh_token,
    }
    is_token_valid = True
    return output, is_token_valid
