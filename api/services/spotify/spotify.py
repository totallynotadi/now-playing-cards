import base64
import os
import time
from typing import Any, Dict, Union
from urllib.parse import quote

import requests
from dotenv import find_dotenv, load_dotenv

# try:
#     from services.utils import singleton
# except (ModuleNotFoundError, ImportError):
#     from api.services.utils import singleton

load_dotenv(find_dotenv())


AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
API_URL = "{}/{}".format(BASE_URL, API_VERSION)

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
REDIRECT_URL = os.getenv("REDIRECT_URL", "")
SCOPES = os.getenv("SCOPES", "")


# @singleton
class SpotifyUtils:
    def __init__(self) -> None:
        pass

    def get_auth_url(self):
        auth_headers = {
            "response_type": "code",
            "redirect_uri": REDIRECT_URL,
            "scope": SCOPES,
            "client_id": CLIENT_ID,
        }

        auth_headers = "&".join(
            ["{}={}".format(param, quote(val)) for param, val in auth_headers.items()]
        )
        auth_url = "{}/?{}".format(AUTH_URL, auth_headers)

        return auth_url

    def get_user_tokens(self, auth_token):
        code_payload = {
            "grant_type": "authorization_code",
            "code": auth_token,
            "redirect_uri": REDIRECT_URL,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response_data = requests.post(TOKEN_URL, data=code_payload).json()
        print(response_data)
        return self.parse_tokens(response_data)

    def parse_tokens(self, data, refresh_token=None):
        """parse user tokens data from token URL returned after authentication."""
        print("::::parsing tokens")
        access_token = data["access_token"]
        token_type = data["token_type"]
        expires_in = data["expires_in"]
        expires_at = int(time.time() + expires_in)
        refresh_token = (
            refresh_token if refresh_token is not None else data["refresh_token"]
        )
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "expires_at": expires_at,
        }
        print("::::finished parsing")
        return tokens

    def token_refresh(self, refresh_token: str):
        refresh_payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        headers = base64.b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode("ascii"))
        headers = {"Authorization": "Basic {}".format(headers.decode("ascii"))}

        response = requests.post(
            TOKEN_URL, data=refresh_payload, headers=headers
        ).json()

        print(":::: ", response)

        return self.parse_tokens(response, refresh_token=refresh_token)

    def get_user_info(self, access_token):
        print(":::getting user info")
        auth_header = {"Authorization": "Bearer {}".format(access_token)}
        user_profile_endpoint = "{}/me".format(API_URL)
        data = requests.get(user_profile_endpoint, headers=auth_header)
        print(f"::::{data.text}")
        data = data.json()
        print("::::got user info")
        return data

    def get_now_playing(self, access_token: str) -> Union[Dict[str, Any], None]:
        auth_header = {"Authorization": "Bearer {}".format(access_token)}
        now_playing_endpoint = "{}/me/player/currently-playing".format(API_URL)

        data = requests.get(now_playing_endpoint, headers=auth_header)
        print(":: spotify track data", data)
        # prints()
        print(dir(data))
        if data.status_code == requests.codes["no_content"] or data.text == "":
            print(":: getting recenty played")
            track = self.get_recently_played(access_token)
            print(":: recently played - ", track)
            return track
        else:
            data = data.json()
            track = data["item"]
        return track

    def get_recently_played(self, access_token: str) -> Dict[str, Any]:
        auth_header = {"Authorization": "Bearer {}".format(access_token)}
        recently_played_endpoint = (
            "{}/me/player/recently-played?&after=1484811043508".format(API_URL)
        )
        data = requests.get(recently_played_endpoint, headers=auth_header).json()

        # actual format of data['items'] - dict_keys(['track', 'played_at', 'context'])
        track = data["items"][0]["track"]
        return track


spotify_utils = SpotifyUtils()
