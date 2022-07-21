import base64
import json
import os
import threading
import time
from typing import Dict
from urllib.parse import quote

import firebase_admin
from firebase_admin import credentials, firestore
import flask
import requests
from dotenv import find_dotenv, load_dotenv

try:
    from .builders import now_playing
except ImportError:
    from builders import now_playing


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

FIREBASE_CREDS = json.loads(base64.b64decode(b'eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInJlYWRtZS1ub3ctcGxheWluZyIsICJwcml2YXRlX2tleV9pZCI6ICI4NzUwMTU0M2YwZGQ1OWZlNGQxYzJlMzAxODIxNGQyNDRkOWJkYzUwIiwgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZRSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2N3Z2dTakFnRUFBb0lCQVFDWnJ6U1g2T3N5Ujd3WlxuNzMydlBQUTExQXRZMm8wbnB2emFRLzhjb1ZXdldaRTlJUzBaZitYU0IyNy80bitTczlsdEw5bUF2a1h5dnhHK1xueE9JTTRGeWVJc2FYcTJEcU9LazlSSisrWUFteHNibnVEa29LaDRsYmJRc3J3MklYTUIweGZUZC91Y3U5dDZLVVxubnN5Mzk0N2tpRWJTaGpYMGJVT2RDU210bGF5V3cxc2QxWmNLMWZwdHRqM0ptWlgzUS9iZlVWNlUxcHZmbE03SVxuMjZFYVR2eTJXTVBWSjRyM1BvbXBHUGdNVWFIaVhHSmwzRSsySVg0cFMrSExhS3NUSjRRemRvZTVVWldEUkxiZ1xuVGFzWG9IKzVFZlVURnVtMFIwQk41eDY0Vm5VZnM5bUVISlRDOW9aQWw3UnRpY25uazNiZlkvcG5JSTdUelNMOVxuOVNueXZkTzVBZ01CQUFFQ2dnRUFFQ1c3WlF3ckhTSHlJcmY1K00zeTIwNkRvREw3WW91T05Pa3d6bXRwcHpaR1xuRnpvTGhPcStKUlNVbmpSb1FzdmNpQmMvVjBKMnMwQU4zMkZNbm4xNjRiOGw1bFR5aG4yTVU2U0lrNzQvdW9EQlxuMkVBK1dZK2UyQ0V6aTZZNFlkY1RkQ29UeVJybWpERVZseCs5d3dVUzZaSmpmWlp1S0JmTVl6MHRtTUJaalZBQVxuM1orcjJ4d0VtSVVXUjNLbVZWK2RDWXBTdEt0RDN0SDY2dFRxbStFcTlHQUdWN29DTFpNNHZjZ2FvcnZwL05sWFxuUjRzM2JrL3YwbHFlaGdISEJjUnpFWXJLdytZRm1wNTJXdTA4aEpnVjlGWEJzdWJvbVlQMXRhclZjcG9va0IzWlxuNHNoR1hRNVVIekpybHRYaDZOTTZmZnI2aERYejBzQzN0cEY5RFlqVTRRS0JnUURScFFwckgyL1FUMTJMZUpPQ1xuTmVjZ3o5SFdhOGRVTVlLZHU5TGhwaFZlZjQyWUxVbzhJbVd6MWI4dzlST3cxTWJWTHRSdlIyM2hmVUsvWjd0MFxuNDJRMTNRM0lLL3ZwZnp0bXlZYkZZS3FlQjhRMnR4ck5ZZFRPWXFGcU1CV3B5L2RPcFpjaFhHTWFXcGFVamVWWlxuZU5JQ3ZvNVdJOC9TdXhnTDdhQWNTQWZiWVFLQmdRQzdxb2JMSXNzdXFFNDZyK2RNTWRPajcxRWdDU0FRYjRMdFxucU42OVM4WmZyemVYUFB3TEd0R2prT2t0NDFxcjcxTEpCaVIyWjlhRmVmSWQzMHR6d3A2MHhxVGozaExaanNSQVxuZVZBSndDMDVKcTNvSDFXOXN0NldEUWNqOFJxVEFJNE9kWGhhcmVPanJyT0NwM2FsVzBGczhmcGIrQU50YXFHWlxuM01YK2loUHZXUUtCZ0JIRVBOZkxPRHlkSFQ1ZW41R2ZZOUVDQzdSeU9kaEd3ZDBBTitUcm9FLzcyMUlVTklCWVxuSWVwVnFQaExMTG9Gcmp3TzFlNEFUYTJZWWZtNm5zWlBKd1R4a09OdjVzOW8rdTNCRW16VHZtSGFJcVRJYTdzUVxuR1dyTUxRWEV3WEU4V2Q4T1pYcHNTL0hGejVFVFhXWnh1TXFHdjZWSkw2bWFOWFY5VTk1UnRHakJBb0dBVC9BWFxuY3JmamJJQnNzanJ6ZjFWS0hXNTNVL29QR25FbGlDNkNrb2VRZkhtYWFHV2x4dVVwbjA2K3hMa3Zpa1ZyTWczWFxud2tnQTdPSkE2OUNOeDBXRGJPV2dueCtkVCthc1dmcFN5WlIrcnZWMjVvVlNkSGVZc0xuajdMOXEzbXRDRjQ2YVxuTWFZWWJVU2hXbW9TOCtTblBjemxJLy9GRmZweDA2UmpBa1cyc0NFQ2dZRUFsZXlpR2RwZ3dVcnE5VGd6Y0txTFxuUmNpTXRJa1RGNmc4bWJ3N256OUVFalB5WnZCdHhGVVd5ZFNTNVpyVHNYc1lZbWFvWUpLVVlrZkl0NHlIS0llSlxuMGNPTEVKZStFbVVhRnVGWjZFRk1zSFBkdmlEWjJ6MzlZMG1BMmxKNnpGQnU0RlhyalBRMHJPNm40NnRCREZWdFxuekFTYUhEdlo5S0FVZHhsN2pSQlgwUVE9XG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLCAiY2xpZW50X2VtYWlsIjogImZpcmViYXNlLWFkbWluc2RrLWNpa20yQHJlYWRtZS1ub3ctcGxheWluZy5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJjbGllbnRfaWQiOiAiMTE0OTE4NTEyMDU5MDg5NTY5ODU4IiwgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvZmlyZWJhc2UtYWRtaW5zZGstY2lrbTIlNDByZWFkbWUtbm93LXBsYXlpbmcuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20ifQ=='))


app = flask.Flask(__name__)
users = {}

creds = credentials.Certificate(FIREBASE_CREDS)
firebase_admin.initialize_app(creds)

db = firestore.client().collection('users')


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/login')
def login():
    auth_headers = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URL,
        "scope": SCOPES,
        "client_id": CLIENT_ID
    }

    auth_headers = '&'.join(['{}={}'.format(param, quote(val)) for param, val in auth_headers.items()])
    auth_url = "{}/?{}".format(AUTH_URL, auth_headers)
    print(auth_url)
    return flask.redirect(auth_url)


def parse_tokens(data):
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    token_type = data['token_type']
    expires_in = data['expires_in']
    expires_at = int(time.time() + expires_in)
    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in,
        'expires_at': expires_at
    }
    return tokens


@app.route('/callback/q')
def callback():
    auth_token = flask.request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URL,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    post_request = requests.post(TOKEN_URL, data=code_payload)

    response_data = json.loads(post_request.text)

    tokens = parse_tokens(response_data)

    data = get_user_info(tokens['access_token'])

    if not data['id'] in users:
        users[data['id']] = tokens
    
    save_tokens(data['id'], tokens)

    return flask.render_template('success.html', page_result='Login Successful', user_id=data.get('id'))


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


def save_tokens(uid, user_tokens):
    user = db.document(uid)
    user.set(user_tokens)


def check_token_expiry(uid, user_tokens):
    if int(time.time()) >= user_tokens['expires_at'] - 60:
        user_tokens = token_refresh(user_tokens['refresh_token'])
        user_tokens = parse_tokens(user_tokens)
        threading._start_new_thread(save_tokens, (uid, user_tokens, ))
    users[uid] = user_tokens
    return user_tokens


def get_access_token(uid):
    if uid in users:
        user_tokens = users[uid]
    else:
        user = db.document(uid).get()
        if not user.exists:
            return None
        user_tokens = user.to_dict()
    user_tokens = check_token_expiry(uid, user_tokens)
    return user_tokens.get('access_token', None)


def get_user_info(access_token):
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    user_profile_endpoint = '{}/me'.format(API_URL)
    data = requests.get(user_profile_endpoint, headers=auth_header).json()
    return data


def get_now_playing(access_token):
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    now_playing_endpoint = '{}/me/player/currently-playing'.format(API_URL)

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


@app.route('/now-playing/q')
def now_playing_endpoint():
    params = flask.request.args

    # temporary card for testing
    if params.get('test') == 'true':
        with open('cards/test-re.svg', 'r', encoding='utf-8') as file:
            template = file.read()
        response = flask.Response(template, mimetype='image/svg+xml')
        return response

    user_id = params.get('uid')

    access_token = get_access_token(user_id)
    if access_token is None:
        return "User Not Found, please login before usage"

    track = get_now_playing(access_token)
    if track is None:
        print(f":::getting recently played tracks")
        track = get_recently_played(access_token)
        print(f":::track-keys: {track.keys()}")

    size = params.get('size', 'med')
    if size not in ['default', 'small', 'med', 'large']:
        size = 'med'

    with open(f'api/cards/card_{size}.svg', 'r', encoding='utf-8') as file:
        svg_template = str(file.read())

    text_theme = params.get('theme', 'light')
    background_theme = params.get('background', 'dark')

    card = now_playing.build(
        track, svg_template, background_theme, text_theme, size)
    card = card.replace("&", "&amp;")

    response = flask.Response(card, mimetype='image/svg+xml')
    response.headers["Cache-Control"] = "s-maxage=1"
    return response


@app.route('/users')
def get_users():
    return flask.jsonify(users)


if __name__ == '__main__':
    # REDIRECT_URL = 'https://localhost:8080/callback/q'
    app.run(debug=True, host='localhost', ssl_context='adhoc')
