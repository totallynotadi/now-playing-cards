import base64
import json
import threading
import time
from typing import Dict
from urllib.parse import quote

import firebase_admin
import flask
import requests
from dotenv import find_dotenv, load_dotenv
from firebase_admin import credentials, firestore

try:
    from . import spotify
    from .builders import now_playing, utils, themes
except ImportError:
    import spotify
    from builders import now_playing, utils, themes


load_dotenv(find_dotenv())


FIREBASE_CREDS = json.loads(base64.b64decode(b'eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInJlYWRtZS1ub3ctcGxheWluZyIsICJwcml2YXRlX2tleV9pZCI6ICI4NzUwMTU0M2YwZGQ1OWZlNGQxYzJlMzAxODIxNGQyNDRkOWJkYzUwIiwgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZRSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2N3Z2dTakFnRUFBb0lCQVFDWnJ6U1g2T3N5Ujd3WlxuNzMydlBQUTExQXRZMm8wbnB2emFRLzhjb1ZXdldaRTlJUzBaZitYU0IyNy80bitTczlsdEw5bUF2a1h5dnhHK1xueE9JTTRGeWVJc2FYcTJEcU9LazlSSisrWUFteHNibnVEa29LaDRsYmJRc3J3MklYTUIweGZUZC91Y3U5dDZLVVxubnN5Mzk0N2tpRWJTaGpYMGJVT2RDU210bGF5V3cxc2QxWmNLMWZwdHRqM0ptWlgzUS9iZlVWNlUxcHZmbE03SVxuMjZFYVR2eTJXTVBWSjRyM1BvbXBHUGdNVWFIaVhHSmwzRSsySVg0cFMrSExhS3NUSjRRemRvZTVVWldEUkxiZ1xuVGFzWG9IKzVFZlVURnVtMFIwQk41eDY0Vm5VZnM5bUVISlRDOW9aQWw3UnRpY25uazNiZlkvcG5JSTdUelNMOVxuOVNueXZkTzVBZ01CQUFFQ2dnRUFFQ1c3WlF3ckhTSHlJcmY1K00zeTIwNkRvREw3WW91T05Pa3d6bXRwcHpaR1xuRnpvTGhPcStKUlNVbmpSb1FzdmNpQmMvVjBKMnMwQU4zMkZNbm4xNjRiOGw1bFR5aG4yTVU2U0lrNzQvdW9EQlxuMkVBK1dZK2UyQ0V6aTZZNFlkY1RkQ29UeVJybWpERVZseCs5d3dVUzZaSmpmWlp1S0JmTVl6MHRtTUJaalZBQVxuM1orcjJ4d0VtSVVXUjNLbVZWK2RDWXBTdEt0RDN0SDY2dFRxbStFcTlHQUdWN29DTFpNNHZjZ2FvcnZwL05sWFxuUjRzM2JrL3YwbHFlaGdISEJjUnpFWXJLdytZRm1wNTJXdTA4aEpnVjlGWEJzdWJvbVlQMXRhclZjcG9va0IzWlxuNHNoR1hRNVVIekpybHRYaDZOTTZmZnI2aERYejBzQzN0cEY5RFlqVTRRS0JnUURScFFwckgyL1FUMTJMZUpPQ1xuTmVjZ3o5SFdhOGRVTVlLZHU5TGhwaFZlZjQyWUxVbzhJbVd6MWI4dzlST3cxTWJWTHRSdlIyM2hmVUsvWjd0MFxuNDJRMTNRM0lLL3ZwZnp0bXlZYkZZS3FlQjhRMnR4ck5ZZFRPWXFGcU1CV3B5L2RPcFpjaFhHTWFXcGFVamVWWlxuZU5JQ3ZvNVdJOC9TdXhnTDdhQWNTQWZiWVFLQmdRQzdxb2JMSXNzdXFFNDZyK2RNTWRPajcxRWdDU0FRYjRMdFxucU42OVM4WmZyemVYUFB3TEd0R2prT2t0NDFxcjcxTEpCaVIyWjlhRmVmSWQzMHR6d3A2MHhxVGozaExaanNSQVxuZVZBSndDMDVKcTNvSDFXOXN0NldEUWNqOFJxVEFJNE9kWGhhcmVPanJyT0NwM2FsVzBGczhmcGIrQU50YXFHWlxuM01YK2loUHZXUUtCZ0JIRVBOZkxPRHlkSFQ1ZW41R2ZZOUVDQzdSeU9kaEd3ZDBBTitUcm9FLzcyMUlVTklCWVxuSWVwVnFQaExMTG9Gcmp3TzFlNEFUYTJZWWZtNm5zWlBKd1R4a09OdjVzOW8rdTNCRW16VHZtSGFJcVRJYTdzUVxuR1dyTUxRWEV3WEU4V2Q4T1pYcHNTL0hGejVFVFhXWnh1TXFHdjZWSkw2bWFOWFY5VTk1UnRHakJBb0dBVC9BWFxuY3JmamJJQnNzanJ6ZjFWS0hXNTNVL29QR25FbGlDNkNrb2VRZkhtYWFHV2x4dVVwbjA2K3hMa3Zpa1ZyTWczWFxud2tnQTdPSkE2OUNOeDBXRGJPV2dueCtkVCthc1dmcFN5WlIrcnZWMjVvVlNkSGVZc0xuajdMOXEzbXRDRjQ2YVxuTWFZWWJVU2hXbW9TOCtTblBjemxJLy9GRmZweDA2UmpBa1cyc0NFQ2dZRUFsZXlpR2RwZ3dVcnE5VGd6Y0txTFxuUmNpTXRJa1RGNmc4bWJ3N256OUVFalB5WnZCdHhGVVd5ZFNTNVpyVHNYc1lZbWFvWUpLVVlrZkl0NHlIS0llSlxuMGNPTEVKZStFbVVhRnVGWjZFRk1zSFBkdmlEWjJ6MzlZMG1BMmxKNnpGQnU0RlhyalBRMHJPNm40NnRCREZWdFxuekFTYUhEdlo5S0FVZHhsN2pSQlgwUVE9XG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLCAiY2xpZW50X2VtYWlsIjogImZpcmViYXNlLWFkbWluc2RrLWNpa20yQHJlYWRtZS1ub3ctcGxheWluZy5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJjbGllbnRfaWQiOiAiMTE0OTE4NTEyMDU5MDg5NTY5ODU4IiwgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvZmlyZWJhc2UtYWRtaW5zZGstY2lrbTIlNDByZWFkbWUtbm93LXBsYXlpbmcuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20ifQ=='))


app = flask.Flask(__name__)
users = {}

creds = credentials.Certificate(FIREBASE_CREDS)
firebase_admin.initialize_app(creds)

db = firestore.client().collection('users')


def check_token_expiry(uid, user_tokens):
    if int(time.time()) >= user_tokens['expires_at'] - 60:
        refresh_token = user_tokens['refresh_token']
        user_tokens = spotify.token_refresh(refresh_token)
        user_tokens = spotify.parse_tokens(user_tokens, refresh_token)
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


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/login')
def login():
    auth_headers = {
        "response_type": "code",
        "redirect_uri": spotify.REDIRECT_URL,
        "scope": spotify.SCOPES,
        "client_id": spotify.CLIENT_ID
    }

    auth_headers = '&'.join(['{}={}'.format(param, quote(val))
                            for param, val in auth_headers.items()])
    auth_url = "{}/?{}".format(spotify.AUTH_URL, auth_headers)
    print(auth_url)
    return flask.redirect(auth_url)


@app.route('/callback/q')
def callback():
    print('in callback')
    auth_token = flask.request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": spotify.REDIRECT_URL,
        'client_id': spotify.CLIENT_ID,
        'client_secret': spotify.CLIENT_SECRET,
    }

    response_data = requests.post(spotify.TOKEN_URL, data=code_payload).json()
    print(f"::::response data - {response_data}")

    tokens = spotify.parse_tokens(response_data)

    data = spotify.get_user_info(tokens['access_token'])

    if not data['id'] in users:
        users[data['id']] = tokens

    save_tokens(data['id'], tokens)

    return flask.render_template('success.html', page_result='Login Successful', user_id=data.get('id'))


def save_tokens(uid, user_tokens):
    user = db.document(uid)
    user.set(user_tokens)


@app.route('/now-playing/q')
def now_playing_endpoint():
    params = flask.request.args

    # temporary card for testing
    if params.get('test', 'false') == 'true':
        with open('api/cards/card_small_docs.svg', 'r', encoding='utf-8') as file:
            template = file.read()
        response = flask.Response(template, mimetype='image/svg+xml')
        return response

    user_id = params.get('uid')

    access_token = get_access_token(user_id)
    if access_token is None:
        return "User Not Found, please login before usage"

    track = spotify.get_now_playing(access_token)
    try:
        track['image']: requests.Response = requests.get(track['album'].pop('images')[0]['url'])
    except (TypeError, Exception):
        print(track)
        print(track.keys())
    if track is None:
        print(f":::getting recently played tracks")
        track = spotify.get_recently_played(access_token)
        print(f":::track-keys: {track.keys()}")

    theme, template, size = utils.parse_params(params)
    if str(theme['background']) == 'extract':
        color = utils.get_image_color(track['image'])

        theme['background'] = utils.rgb_to_hex(color)
        print(theme)
        if utils.is_light(color):
            theme['text'] = themes.text_theme_dark
        else:   theme['text'] = themes.text_theme_light

    card = now_playing.build(track, theme, template, size)
    card = card.replace("&", "&amp;")

    response = flask.Response(card, mimetype='image/svg+xml')
    response.headers["Cache-Control"] = "s-maxage=1"
    return response


@app.route('/users')
def get_users():
    return flask.jsonify(users)


if __name__ == '__main__':
    REDIRECT_URL = 'https://localhost:5000/callback/q'
    app.run(debug=True, host='localhost', ssl_context='adhoc')
