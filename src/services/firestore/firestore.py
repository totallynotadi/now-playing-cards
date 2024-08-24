import base64
import json
import os
import time
from typing import Any

import firebase_admin  # type: ignore
from dotenv import find_dotenv, load_dotenv
from firebase_admin import credentials, firestore

from ..spotify.spotify import SpotifyUtils
from ..utils import singleton

load_dotenv(find_dotenv())


@singleton
class FirestoreUtils:
    def __init__(self) -> None:
        self.spotify_utils: SpotifyUtils = SpotifyUtils()
        if os.getenv("FIREBASE_CREDS", "") == "":
            raise ValueError("::missing environment variables for Firebase")

        firebase_creds = os.getenv("FIREBASE_CREDS", "")
        print(f':: FIREBASE CREDS - {firebase_creds}')
        print(":: BYTES_JSON - ", base64.b64decode(firebase_creds))
        FIREBASE_CREDS = json.loads(
            base64.b64decode(
                bytes(os.getenv("FIREBASE_CREDS", ""), encoding="utf-8"))
        )
        creds = credentials.Certificate(FIREBASE_CREDS)
        app = firebase_admin.initialize_app(creds)

        self.users: Any = firestore.client(app).collection("users")
        self.current_user: Any = None

    def save_tokens(self, uid, user_tokens):
        print("::saving tokens")
        self.current_user = self.users.document(uid)
        self.current_user.set(user_tokens)
        print("::finished saving tokens")

    def check_token_expiry(self, uid, user_tokens):
        if int(time.time()) >= user_tokens["expires_at"] - 60:
            refresh_token = user_tokens["refresh_token"]
            user_tokens = self.spotify_utils.token_refresh(refresh_token)
            self.save_tokens(uid, user_tokens)
        return user_tokens

    def get_access_token(self, uid):
        self.current_user = self.users.document(uid).get()
        if not self.current_user.exists:
            return None
        user_tokens = self.current_user.to_dict()
        user_tokens = self.check_token_expiry(uid, user_tokens)
        return user_tokens.get("access_token", None)
