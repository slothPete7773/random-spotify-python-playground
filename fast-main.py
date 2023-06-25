import json
import time
import configparser
config = configparser.ConfigParser()
config.read("env.conf")
# value_a = config.get("test", "a")

import spotipy
from pydantic import BaseModel, Field, EmailStr
from spotipy.oauth2 import SpotifyOAuth
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
app = FastAPI()

CLIENT_ID="cbe1c38fa78c4420be783075886f43a3"
CLIENT_SECRET="f5b0ee9fce764f66b22fcc03e1a0ff9e"
REDIRECT_URI="http://localhost:8000/authorization"
# A list of space-separated scopes
SCOPE = "user-read-playback-state" 

# Route methods
@app.get("/")
async def _root(token: str=None):
    # if (token):
    #     token = token.replace("'", '"')
    #     _token = json.loads(token)
    # else:
    #     _token = "Empty"

    _token, is_valid = get_access_token()
    print(is_valid)
    print(_token)
    return {
        "greet": "Hello World",
        "page": "/",
        "_token": _token if is_valid else "Empty",
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

@app.get("/spotify-api/me")
async def _me(token: str=None):
    pass

# Utility functions
def create_spotify_oauth():
    oauth_instance = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE 
    )

    return oauth_instance

# This function is wrong, 
# it should get just on value, cannot get the whole token_info in just one call
def get_access_token() -> tuple[dict, bool]:
    access_token_info = {}
    is_token_valid = False
    # If token is not cached, return false
    if not (config.has_section("token_info")):
        is_token_valid = False
        return access_token_info, is_token_valid
    else:
        access_token_info = config.get("token_info", "access_token")
    
    # Check if the token has expired
    now = int(time.time())
    is_token_expired = int(config.get('token_info', 'expires_at')) - now < 60

    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        refresh_token = config.get('token_info', 'refresh_token')
        token_info = sp_oauth.refresh_access_token(refresh_token)
        config.set("token_info", "access_token", token_info['access_token'])
        config.set("token_info", "token_type", token_info['token_type'])
        config.set("token_info", "expires_in", str(token_info['expires_in']))
        config.set("token_info", "scope", token_info['scope'])
        config.set("token_info", "expires_at", str(token_info['expires_at']))
        config.set("token_info", "refresh_token", token_info['refresh_token'])

        access_token_info = token_info['access_token']

    is_token_valid = True
    return access_token_info, is_token_valid
    # Return token if exists and not expire 
