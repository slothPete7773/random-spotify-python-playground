import json
import time
import configparser
config = configparser.ConfigParser()
config.read("env.conf")
# value_a = config.get("test", "a")

import spotipy
from pydantic import BaseModel, Field, EmailStr
from spotipy.oauth2 import SpotifyOAuth

from typing import Annotated
from fastapi import FastAPI, Path, Request, HTTPException
from fastapi.responses import RedirectResponse
app = FastAPI()

CLIENT_ID="cbe1c38fa78c4420be783075886f43a3"
CLIENT_SECRET="f5b0ee9fce764f66b22fcc03e1a0ff9e"
REDIRECT_URI="http://localhost:8000/authorization"
# A list of space-separated scopes
SCOPE = "user-top-read" 

# Route methods
@app.get("/")
async def _root(token: str=None):
    _token, is_token_valid = get_access_token()
    _expires_at, is_expires_valid = get_expires_at()
    # print(is_valid)
    # print(_token)
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
    return RedirectResponse(url=f"/")

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

    access_token = config.get("token_info", "access_token")
    token_type = config.get("token_info", "token_type")
    expires_in = config.get("token_info", "expires_in")
    scope = config.get("token_info", "scope")
    expires_at = config.get("token_info", "expires_at")
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
    print(f"token_info: {token_info}")
    return output, is_token_valid

