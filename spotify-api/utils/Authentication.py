# from pathlib import Path
import urllib3 
from typing import Dict, Type, Optional
from dataclasses import dataclass
import base64
import datetime
import requests

import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
# from spotipy.exceptions import 


import configparser
config = configparser.ConfigParser()

from pydantic import BaseModel

# class SpotifyInstance(BaseModel):
@dataclass
class SpotifyInstance:
    status: int
    instance: Optional[Spotify] = None
    description: Optional[str] = None

class Authenticator():

    def __init__(self, config_file) -> None:
        config.read(config_file)

        client_id = config.get("spotify_credential", "client_id")
        client_secret = config.get("spotify_credential", "client_secret")
        redirect_uri = config.get("spotify_credential", "redirect_uri")
        

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "user-top-read user-read-currently-playing user-read-recently-played user-read-private user-read-email"
        self.state = ""
        self.show_dialog = ""
        self.auth_code = ""
        self.tokens = {}
        self.spotify_instance = object()
        self.oauth_instance = object()
        self.config = config
        self.config_file = config_file

        self.OAUTH_ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
        self.API_v1_URL = "https://api.spotify.com/v1"

    def print_something(self):
        # print("state:", self.state)
        # print(f"type oauth: {type(self.oauth_instance)}")
        print(f"isinstance(self.oauth_instance, SpotifyOAuth): [{isinstance(self.oauth_instance, SpotifyOAuth)}]")

    def get_client_key_base64(self) -> str: 
        return base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

    def get_oauth_instance(self) -> SpotifyOAuth:
        # print(f"isinstance(self.oauth_instance, SpotifyOAuth): [{isinstance(self.oauth_instance, SpotifyOAuth)}]")

        if not isinstance(self.oauth_instance, SpotifyOAuth):
        # type(self.oauth_instance) != type(SpotifyOAuth):
            print("oauth not yet create, creating one now")
            _oauth_instance = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope
            )
            self.oauth_instance = _oauth_instance
        return self.oauth_instance

    def get_spotify_instance(self) -> SpotifyInstance:
        if self.spotify_instance is spotipy.Spotify:
            return SpotifyInstance(200, self.spotify_instance)
        # {
        #         "status": 200,
        #         "instance": self.spotify_instance
        #     }

        try:
            self.spotify_instance = spotipy.Spotify(oauth_manager=self.oauth_instance)
        except spotipy.SpotifyOauthError("Failed to instantiate Spotify instance") as e:
            raise e
        return SpotifyInstance(200, self.spotify_instance)
    # {
    #         "status": 200,
    #         "instance": self.spotify_instance,
    #     }
    
    def get_access_token(self, code: str = None) -> str: 
        is_authorize: str = self.config.get("token_info", "authorize?")
        prev_scope = set(self.config.get("token_info", "scope").split(" "))
        curr_scope = set(self.scope.split(" "))
        if ((is_authorize.lower() == "true") and (curr_scope == prev_scope)):
            print("already true, give access_token")
            return self.config.get("token_info", "access_token")
        CLIENT_KEY_B64: str = self.get_client_key_base64() # base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(CLIENT_KEY_B64)
        }
        payload: dict = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        OAUTH_ACCESS_TOKEN_URL: str = self.OAUTH_ACCESS_TOKEN_URL
        r = requests.post(OAUTH_ACCESS_TOKEN_URL, headers=headers, data=payload)
        token_info = r.json()
        print(f"Token Info: \n{token_info}")
            # token_info = self.oauth_instance.get_access_token(code)
        # except Exception as e:
        #     raise e
        
        self.config.set("token_info", "access_token", token_info["access_token"])
        self.config.set("token_info", "token_type", token_info["token_type"])
        self.config.set("token_info", "expires_in", str(token_info["expires_in"]))
        self.config.set("token_info", "scope", token_info["scope"])
        expires_at = (datetime.datetime.now() + datetime.timedelta(seconds=token_info["expires_in"])).timestamp()
        self.config.set("token_info", "expires_at", str(expires_at))
        self.config.set("token_info", "refresh_token", token_info["refresh_token"])
        self.config.set("token_info", "authorize?", "true")
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)
            # self.oauth_instance.
        return token_info["access_token"]

    # def extend
    def refresh_access_token(self) -> dict:
        is_authorize: str = self.config.get("token_info", "authorize?")
        if (is_authorize.lower() == "false"):
            raise PermissionError
        
        payload: dict = {
            "grant_type": "refresh_token",
            "refresh_token": f'{self.config.get("token_info", "refresh_token")}'
        }

        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(self.get_client_key_base64())
        }
        r = requests.post(self.OAUTH_ACCESS_TOKEN_URL, headers=headers, data=payload)
        token_info = r.json()

        # try: 
        # _expire_timestamp = self.config.get("token_info", "expires_at")
        # old_expire_timestamp = datetime.datetime.utcfromtimestamp(float(_expire_timestamp))
        print(f"Time now: {datetime.datetime.now()}")
        new_expire_dt = datetime.datetime.now() + datetime.timedelta(seconds=token_info['expires_in'])
        new_expire_stamp = new_expire_dt.timestamp()
        # new_expire_timestamp = old_expire_timestamp + _expire_timestamp
        print(f"new expire date: {new_expire_dt}")
        print(f"new expire : {new_expire_stamp}")
        print(f"recovered expire : {datetime.datetime.fromtimestamp(new_expire_stamp)}")
                              
                              #utcfromtimestamp(float(new_expire_stamp))}")

        self.config.set("token_info", "expires_at", str(new_expire_stamp))
        self.config.set("token_info", "access_token", token_info["access_token"])
        with open(self.config_file, 'w') as config_file:
                self.config.write(config_file)

        return token_info
    
    def is_token_near_expires_in_15_min(self):
        _expire_timestamp = self.config.get("token_info", "expires_at")
        expire_timestamp = datetime.datetime.fromtimestamp(float(_expire_timestamp))
        target_time = expire_timestamp - datetime.timedelta(minutes=15)
        return  target_time < datetime.datetime.now()
        

    def get_current_user(self):
        access_token = self.get_access_token()
        headers: dict = {
            "Authorization": f"Bearer {access_token}"
        }
        try: 
            r = requests.get(f"{self.API_v1_URL}/me", headers=headers, timeout=10)
            print(r)
            response = r.json()

        except Exception as error:
            raise error

        return {
            "status": 200,
            "response": response
        }

    def get_recently_listened(self):
        pass

    def get_currently_listening(self) -> Dict:
        access_token = self.get_access_token()
        headers: dict = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            API_URL = f"{self.API_v1_URL}/me/player/currently-playing"
            # params = 
            response = requests.get(API_URL, headers=headers, timeout=10)
            # print(response.status_code)
            # print(type(response))
            # response = response.json()
        except Exception as error:
            raise error
        
        if (response.status_code == 204):
            return {
                "status": 204,
                "msg": "No content being played or recently played",
                "response": None
            }
        return {
            "status": 200,
            "response": response.json()
        }


    def get_top_tracks(self):
        pass

    def get_top_artists(self):
        pass

    def get_artist(self):
        pass

    def get_album(self):
        pass

    def get_track(self):
        pass

    def get_genre_of_an_album(self):
        pass

    def get_genre_of_an_artist(self):
        pass