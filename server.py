import json
import time
from urllib.parse import quote
import flask
import requests

app = flask.Flask(__name__)

CLIENT_ID = '2996cf26fcbc4ebc9c30b4b9fbe826d8'
CLIENT_SECRET = '0337d221d0474fd5982368cc3ad9d332'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

BASE_URL = 'https://api.spotify.com'
API_VERSION = 'v1'
API_URL = '{}/{}'.format(BASE_URL, API_VERSION)

SERVER_URL = 'https://127.0.0.1'
PORT = 8080
# REDIRECT_URL = 'https://readme-now-playing/callback/q'
REDIRECT_URL = 'https://localhost:8080/callback/q'
SCOPES = 'user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read'


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
    return flask.render_template('success.html', page_result='Login Successful', user_id=data.get('id'))


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=PORT, ssl_context='adhoc')
