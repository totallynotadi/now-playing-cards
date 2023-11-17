import base64
import json
import os
import time

import firebase_admin
from dotenv import find_dotenv, load_dotenv
from firebase_admin import credentials, firestore

try:
    from services.spotify import spotify_utils
    from services.utils import singleton
except (ModuleNotFoundError, ImportError):
    from api.services.spotify import spotify_utils
    from api.services.utils import singleton

load_dotenv(find_dotenv())


@singleton
class FirestoreUtils:
    def __init__(self) -> None:
        FIREBASE_CREDS = json.loads(
            base64.b64decode(os.getenv("FIREBASE_CREDS", "")[2:-1])
        )
        creds = credentials.Certificate(FIREBASE_CREDS)
        app = firebase_admin.initialize_app(creds)

        self.users = firestore.client(app).collection("users")
        self.current_user = None

    def save_tokens(self, uid, user_tokens):
        print("::saving tokens")
        self.current_user = self.users.document(uid)
        self.current_user.set(user_tokens)
        print("::finished saving tokens")

    def check_token_expiry(self, uid, user_tokens):
        if int(time.time()) >= user_tokens["expires_at"] - 60:
            refresh_token = user_tokens["refresh_token"]
            user_tokens = spotify_utils.token_refresh(refresh_token)
            self.save_tokens(uid, user_tokens)
        return user_tokens

    def get_access_token(self, uid):
        self.current_user = self.users.document(uid).get()
        if not self.current_user.exists:
            return None
        user_tokens = self.current_user.to_dict()
        user_tokens = self.check_token_expiry(uid, user_tokens)
        return user_tokens.get("access_token", None)


firestore_utils = FirestoreUtils()
