import base64
import json
from os import access
import time
from typing import Dict
from urllib.parse import quote

import flask
import requests
try:
    from .utils import load_users
    from .builders import now_playing
except ImportError:
    from utils import load_users
    from builders import now_playing
     

app = flask.Flask(__name__)
users = load_users()

CLIENT_ID = '2996cf26fcbc4ebc9c30b4b9fbe826d8'
CLIENT_SECRET = '0337d221d0474fd5982368cc3ad9d332'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
API_URL = '{}/{}'.format(BASE_URL, API_VERSION)

SERVER_URL = 'https://127.0.0.1'
PORT = 8080
REDIRECT_URL = 'https://readme-now-playing.vercel.app/callback/q'
# REDIRECT_URL = 'https://localhost:8080/callback/q'
SCOPES = 'user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read'


def save_users(*args: Dict[str, Dict[str, str]]):
    for user in args:
        users.update(user)
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file)


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

    auth_headers = '&'.join(['{}={}' .format(param, quote(val))
                            for param, val in auth_headers.items()])
    auth_url = "{}/?{}".format(AUTH_URL, auth_headers)
    print(auth_url)
    return flask.redirect(auth_url)


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

    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    token_type = response_data['token_type']
    expires_in = response_data['expires_in']
    expires_at = int(time.time() + expires_in)

    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    user_profile_endpoint = '{}/me'.format(API_URL)
    data = requests.get(user_profile_endpoint, headers=auth_header)
    data = json.loads(data.text)

    if not data['id'] in users:
        users[data['id']] = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'expires_at': expires_at
        }
        # save_users()

    return flask.render_template('success.html', page_result='Login Successful', user_id=data.get('id'))


def token_refresh(refresh_token: str):
    refresh_payload = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    headers = base64.b64encode(
        (CLIENT_ID + ":" + CLIENT_SECRET).encode("ascii"))
    headers = {"Authorization": "Basic %s" % headers.decode("ascii")}

    response = requests.post(
        TOKEN_URL,
        data=refresh_payload,
        headers=headers
    ).json()

    return response


def check_token_expiry(user_id):
    user_tokens = users.get(user_id)
    if int(time.time()) >= user_tokens['expires_at'] - 60:
        user_tokens = token_refresh(user_tokens['refresh_token'])
        user_tokens['expires_at'] = int(
            time.time()) + user_tokens['expires_in']
        users[user_id] = user_tokens


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

    if params.get('test') == 'true':
        with open('cards/test-re.svg', 'r', encoding='utf-8') as file:
            template = file.read()
        response = flask.Response(template, mimetype='image/svg+xml')
        return response

    user_id = params.get('uid')
    if user_id not in users:
        return 'please login before usage'

    check_token_expiry(user_id)

    user_tokens = users.get(user_id)
    access_token = user_tokens['access_token']

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
    background_theme = params.get('background', 'light')

    card = now_playing.build(track, svg_template, background_theme, text_theme, size)
    card.replace("&", "&amp;")

    response = flask.Response(card, mimetype='image/svg+xml')
    response.headers["Cache-Control"] = "s-maxage=1"
    return response 


@app.route('/users')
def get_users():
    return flask.jsonify(users)


if __name__ == '__main__':
    # REDIRECT_URL = 'https://localhost:8080/callback/q'
    app.run(debug=True, host='localhost', port=PORT, ssl_context='adhoc')
