import base64
import json
import os
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


FIREBASE_CREDS = json.loads(base64.b64decode(bytes(os.getenv('FIREBASE_CREDS')[2:-1], encoding='utf-8')))


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
