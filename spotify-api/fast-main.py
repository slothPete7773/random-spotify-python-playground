# from utils.Authorization import create_spotify_oauth, get_access_token, get_expires_at, get_token_info, get_spotify_instance
import requests
import base64
from utils.Authentication import Authenticator
import configparser
config = configparser.ConfigParser()
config.read("env.conf")

# from utils.Class import Artists, Tracks, Albums

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
app = FastAPI()

CONFIG_FILE_PATH = "./env.conf"
spotify_auth = Authenticator(CONFIG_FILE_PATH)

# Route methods
@app.get("/")
async def _root(token: str = None):
    return {
        "greet": "Hello World",
        "page": "/",
        }

@app.get("/login")
async def _login() -> RedirectResponse:
    spotify_auth.print_something()
    auth_instance = spotify_auth.get_oauth_instance()
    auth_url = auth_instance.get_authorize_url()
    return RedirectResponse(url=auth_url)
    
@app.get("/authorization")
async def _authorization(code: str=None):
    if code is not None:
        access_token = spotify_auth.get_access_token(code)

    return RedirectResponse(url=f"/?token={access_token}")

# @app.get("/spotify-api/v1/me")
# async def _me():
#     # token, is_authorized = get_access_token()
#     # if not(is_authorized):
#     #     return RedirectResponse(url="/")
#     spotify_instance = spotify_auth.get_spotify_instance()

#     sp = get_spotify_instance(token)
#     result = sp.current_user()
#     return result

# @app.get("/spotify-api/v1/me/top/{top_type}")
# async def _top(top_type: str, time_range: int = 'medium_term', limit: int = 20, offset: int = 0):
#     time_ranges = ['short_term', 'medium_term', 'long_term']
#     valid_types = ['artists', 'tracks']
#     if not (top_type in valid_types):
#         raise HTTPException(status_code=400, detail='Invalid path parameter')

#     if not (time_range in time_ranges):
#         raise HTTPException(status_code=400, detail='Invalid provided time_range.')
    
#     if not (limit >= 0 and limit <= 50):
#         raise HTTPException(status_code=400, detail='Invalid range of value limit.')

#     if (offset < 0):
#         raise HTTPException(status_code=400, detail='Offset cannot less than 0.')
    
#     token, is_authorized = get_access_token()
#     if not(is_authorized):
#         return RedirectResponse(url="/login")
    
#     sp = get_spotify_instance(token)
#     if (top_type == 'artists'):
#         result = sp.current_user_top_artists(limit=limit, offset=offset, time_range=time_range)
#     else:
#         result = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)
    
#     return result

# # class Artists(BaseModel):
# #     ids: list[str]

# # EXAMPLE_IDS = ["4YPiq62lEVjRdzhSlNto08", "4YLUMAgNyttwx4hUHgtBtR"]
# @app.post("/spotify-api/v1/artists")
# async def _artists(artists: Artists):
#     token, is_authorized = get_access_token()
#     if not(is_authorized):
#         return RedirectResponse(url="/")
    
#     sp = get_spotify_instance(token)
#     result = sp.artists(artists.ids)
#     return result

# # class Tracks(BaseModel):
# #     ids: list[str]

# # EXAMPLE_IDS = ["5nDIBUarJMA7qlpuiryATA", "1enL3bmUAoP3sE1jp7NGP5"]
# @app.post("/spotify-api/v1/tracks")
# async def _tracks(tracks: Tracks):
#     token, is_authorized = get_access_token()
#     if not(is_authorized):
#         return RedirectResponse(url="/")
    
#     sp = get_spotify_instance(token)
#     result = sp.tracks(tracks.ids)
#     return result

# # class Albums(BaseModel):
# #     ids: list[str]

# # EXAMPLE_IDS = ["29vqF5DQuNIzcYM0tept6C", "20hW2P3VSNJ1A7MwjIJ0Up"]
# @app.post("/spotify-api/v1/albums")
# async def _albums(albums: Albums):
#     token, is_authorized = get_access_token()
#     if not(is_authorized):
#         return RedirectResponse(url="/")
    
#     sp = get_spotify_instance(token)
#     result = sp.albums(albums.ids)
#     return result

# @app.post("/spotify-api/v1/albums/genres")
# async def _albums_genre(albums: Albums):
#     token, is_authorized = get_access_token()
#     if not(is_authorized):
#         return RedirectResponse(url="/")
    
#     sp = get_spotify_instance(token)
#     fetched_albums = sp.albums(albums.ids)
#     albums_genre = []
#     for album in fetched_albums['albums']:
#         _temp = {
#             "album_id" : album['id'],
#             "album_name" : album['name'],
#             "album_genre" : album['genres'] if len(album['genres']) > 0 else None
#             }
#         albums_genre.append(_temp)
    
#     return {
#         "albums_genre": albums_genre
#     }

# @app.post("/spotify-api/v1/artists/genres")
# async def _artists_genre(artists: Artists):
#     token, is_authorized = get_access_token()
#     if not(is_authorized):
#         return RedirectResponse(url="/")
    
#     sp = get_spotify_instance(token)
#     fetched_artists = sp.artists(artists.ids)
#     artists_genre = []
#     for artist in fetched_artists['artists']:
#         _temp = {
#             "artist_id": artist['id'],
#             "artist_name": artist['name'],
#             "artist_genres": artist['genres']
#         }
#         artists_genre.append(_temp)
    
#     return {
#         "artists_genre": artists_genre
#     }

# @app.get("/spotify-api/v1/me/currently_playing")
# async def _currently_playing():
#     """
#     Note: The result
#     """
#     token, is_authorized = get_access_token()
#     if not(is_authorized):
#         return RedirectResponse(url="/")
    
#     sp = get_spotify_instance(token)
#     current_playback = sp.currently_playing()
    
#     return current_playback
    