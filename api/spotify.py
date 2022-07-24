import base64
import os
import time

import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
API_URL = '{}/{}'.format(BASE_URL, API_VERSION)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

REDIRECT_URL = os.getenv('REDIRECT_URL')
# REDIRECT_URL = 'https://localhost:5000/callback/q'

SCOPES = os.getenv('SCOPES')


def parse_tokens(data, refresh_token=None):
    print('::::parsing tokens')
    access_token = data['access_token']
    token_type = data['token_type']
    expires_in = data['expires_in']
    expires_at = int(time.time() + expires_in)
    refresh_token = refresh_token if refresh_token is not None else data['refresh_token']
    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in,
        'expires_at': expires_at
    }
    print('::::finished parsing')
    return tokens


def token_refresh(refresh_token: str):
    refresh_payload = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    headers = base64.b64encode(
        (CLIENT_ID + ":" + CLIENT_SECRET).encode("ascii")
    )
    headers = {"Authorization": "Basic %s" % headers.decode("ascii")}

    response = requests.post(
        TOKEN_URL,
        data=refresh_payload,
        headers=headers
    ).json()

    print(':::: ', response)

    return response


def get_user_info(access_token):
    print(':::getting user info')
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    user_profile_endpoint = '{}/me'.format(API_URL)
    data = requests.get(user_profile_endpoint, headers=auth_header)
    print(f'::::{data.text}')
    data = data.json()
    print('::::got user info')
    return data


def get_now_playing(access_token):
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    now_playing_endpoint = '{}/me/player/currently-playing'.format(
        API_URL)

    data = requests.get(now_playing_endpoint, headers=auth_header)
    if data.status_code == requests.codes['no_content']:
        track = get_recently_played(access_token)
        return track
    else:
        data = data.json()
        track = data['item']
    return track


def get_recently_played(access_token):
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    recently_played_endpoint = '{}/me/player/recently-played'.format(API_URL)
    data = requests.get(recently_played_endpoint, headers=auth_header).json()
    # actual format of data['items'] - dict_keys(['track', 'played_at', 'context'])
    track = data['items'][0]['track']
    return track
