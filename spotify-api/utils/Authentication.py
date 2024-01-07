import base64
import datetime
import requests
import spotipy
# from spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

import configparser
config = configparser.ConfigParser()

from pydantic import BaseModel

# class SpotifyInstance(BaseModel):

class Authenticator():

    def __init__(self, config_file) -> None:
        config.read(config_file)

        client_id = config.get("spotify_credential", "client_id")
        client_secret = config.get("spotify_credential", "client_secret")
        redirect_uri = config.get("spotify_credential", "redirect_uri")
        

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "user-top-read user-read-currently-playing user-read-recently-played"
        self.state = ""
        self.show_dialog = ""
        self.auth_code = ""
        self.tokens = {}
        self.spotify_instance = object()
        self.oauth_instance = object()
        self.config = config
        self.config_file = config_file
    
    def print_something(self):
        # print("state:", self.state)
        # print(f"type oauth: {type(self.oauth_instance)}")
        print(f"isinstance(self.oauth_instance, SpotifyOAuth): [{isinstance(self.oauth_instance, SpotifyOAuth)}]")

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
        # auth_url = _oauth_instance.get_authorize_url()
        # print(f"Authorization URL: {auth_url}")
        return self.oauth_instance

    def get_spotify_instance(self):
        if self.spotify_instance is not spotipy.Spotify:
            self.spotify_instance = spotipy.Spotify(auth_manager=self.oauth_instance)
            return self.spotify_instance
        else:
            return {
                "status": 500,
                "description": "Instance not yet authorized"
            }
    
    def get_access_token(self, code: str = None): 
        is_authorize: str = self.config.get("token_info", "authorize?")
        if (is_authorize.lower() == "true"):
            return self.config.get("token_info", "access_token")
        else:
            if code is None:
                raise PermissionError("Not yet authorized and no authorize code provided.")
            
            # try:
            CLIENT_KEY_B64: str = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
            headers: dict = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic {}".format(CLIENT_KEY_B64)
            }
            payload: dict = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            }
            OAUTH_ACCESS_TOKEN_URL: str = "https://accounts.spotify.com/api/token"
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
            expires_at = int((datetime.datetime.now() + datetime.timedelta(seconds=int(token_info["expires_in"]))).timestamp())
            self.config.set("token_info", "expires_at", str(expires_at))
            self.config.set("token_info", "refresh_token", token_info["refresh_token"])
            self.config.set("token_info", "authorize?", "true")
            with open(self.config_file, 'w') as config_file:
                self.config.write(config_file)
                # self.oauth_instance.
            return token_info["access_token"]

    def refresh_access_token(self):
        pass
    
    def is_token_expires(self):
        pass
    


        
        # try:
        #     _oauth_instance = SpotifyOAuth(
        #         client_id=self.client_id,
        #         client_secret=self.client_secret,
        #         redirect_uri=self.redirect_uri,
        #         scope=self.scope
        #     )
        #     self.oauth_instance = _oauth_instance
        #     self.spotify_instance = spotipy.Spotify(auth_manager=_oauth_instance)

        # except Exception as e:
            # print(e)
        
            
        # spotify_instance = spotipy.Spotify(auth_manager=oauth_instance)
    

    # def get_access_token() -> tuple[str, bool]:
    #     token, is_token_valid = get_token_info()
    #     if is_token_valid:
    #         return token["access_token"], is_token_valid
    #     else:
    #         return "", is_token_valid
        
    # def refresh_access_token(): 
    #     return sp_oauth.refresh_access_token(refresh_token)

    # def get_expires_at() -> tuple[int, bool]:
    #     token, is_token_valid = get_token_info()
    #     if is_token_valid:
    #         return token["expires_at"], is_token_valid
    #     else:
    #         return "", is_token_valid

    # def get_token_info() -> tuple[dict, bool]:
    #     sp_oauth = SpotifyOAuth(
    #         client_id=CLIENT_ID,
    #         client_secret=CLIENT_SECRET,
    #         redirect_uri=REDIRECT_URI,
    #         scope=SCOPE
    #     )
    #     # create_spotify_oauth()
    #     token_info = {}
    #     is_token_valid = False
    #     # If token is not cached, return false
    #     if not (config.has_section("token_info")):
    #         is_token_valid = False
    #         return token_info, is_token_valid
        
    #     # Check if the token has expired
    #     now = int(time.time())
    #     is_token_expired = int(config.get("token_info", "expires_at")) - now < 60

    #     if (is_token_expired):
    #         print("token is expired")
    #         refresh_token = config.get("token_info", "refresh_token")
    #         token_info = sp_oauth.refresh_access_token(refresh_token)
    #         config.set("token_info", "access_token", token_info["access_token"])
    #         config.set("token_info", "token_type", token_info["token_type"])
    #         config.set("token_info", "expires_in", str(token_info["expires_in"]))
    #         config.set("token_info", "scope", token_info["scope"])
    #         config.set("token_info", "expires_at", str(token_info["expires_at"]))
    #         config.set("token_info", "refresh_token", token_info["refresh_token"])


    #     output = {
    #         "access_token": config.get("token_info", "access_token"),
    #         "token_type": config.get("token_info", "token_type"),
    #         "expires_in": config.get("token_info", "expires_in"),
    #         "expires_at": config.get("token_info", "expires_at"),
    #         "refresh_token": config.get("token_info", "refresh_token"),
    #         "scope": config.get("token_info", "scope"),
    #     }
    #     is_token_valid = True
    #     return output, is_token_valid

