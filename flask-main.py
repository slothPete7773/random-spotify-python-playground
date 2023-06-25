import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, session, request, redirect

app = Flask(__name__)
app.secret_key = "rndjeqkjrk2j3kj23mkfj400d-s"
app.config['SESSION_COOLIE_NAME'] = 'spotify-session'

CLIENT_ID="cbe1c38fa78c4420be783075886f43a3"
CLIENT_SECRET="f5b0ee9fce764f66b22fcc03e1a0ff9e"
REDIRECT_URI="http://localhost:8000/authorization"
# A list of space-separated scopes
SCOPE = "user-read-playback-state" 

@app.route('/')
def _root():
    keys = session.keys()
    # print(f"session = {session}")
    # print(f"session-keys = {keys}")
    obj = {
        "session": session,
        "session-keys": keys
    }
    print(obj)
    return "<p>Hello World</p>"

@app.route('/login')
def _login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(f'auth_url = {auth_url}')
    return redirect(auth_url)

@app.route('/authorization')
def _authorization():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/')

# Utilities Functions
def get_token():
    is_token_valid = False
    token_info = session.get("token_info", {})
    if not session.get('token_info', 'False'):
        is_token_valid = False
        return token_info, is_token_valid
    
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        refresh_token = session.get('token_info').get('refresh_token')
        token_info = sp_oauth.refresh_access_token(refresh_token)
    
    is_token_valid = True
    return token_info, is_token_valid
    

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )