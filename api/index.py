from dataclasses import asdict

import flask
import requests

from src.services.firestore import FirestoreUtils
from src.services.spotify import SpotifyUtils
from src.utils import parse_params

app = flask.Flask(__name__)
spotify_utils = SpotifyUtils()
firestore_utils = FirestoreUtils()

@app.route("/")
def home():
    return flask.render_template("index.html")


@app.route("/login")
def login():
    return flask.redirect(spotify_utils.get_auth_url())


@app.route("/callback/q")
def callback():
    print("in callback")
    auth_token = str(flask.request.args["code"])

    user_tokens = spotify_utils.get_user_tokens(auth_token=auth_token)

    data = spotify_utils.get_user_info(user_tokens["access_token"])

    firestore_utils.save_tokens(data["id"], user_tokens)

    return flask.render_template(
        "success.html", page_result="Login Successful", user_id=data.get("id")
    )


@app.route("/now-playing/q")
def now_playing_endpoint():
    params = flask.request.args.to_dict()
    params["background_color"] = params.pop("bg-color", str())
    params["text_color"] = params.pop("text-color", str())

    # TO-DO - catch intialization error (for when some params are incorrect). use pydantic for validation
    query_params = QueryParams(**params)  # type: ignore
    print(":: got query params")

    access_token = firestore_utils.get_access_token(query_params.uid)
    if access_token is None:
        return "User Not Found, please login before usage"
    print(":: got access token")

    track = spotify_utils.get_now_playing(access_token)
    print(":: track - ", type(track))

    if track is None:
        print("  :: track is None")
        track = spotify_utils.get_recently_played(access_token)
    print(":: got spotify track", track)

    print(":: getting image")
    image = requests.get(track["album"].pop("images")[0]["url"]).content
    track["image"] = image
    print(":: got image")

    card_data = parse_params(query_params, track)

    print(":: card data", card_data.__dict__)

    card = flask.render_template(
        "cards/card_%s.svg.j2" % query_params.size,
        **asdict(card_data),
    )
    card = card.replace("&", "&amp;")

    response = flask.Response(card, mimetype="image/svg+xml")
    response.headers["Cache-Control"] = "s-maxage=1"
    return response


@app.route("/test")
def test():
    return flask.render_template("cards/card_small.svg.j2")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", ssl_context="adhoc")
