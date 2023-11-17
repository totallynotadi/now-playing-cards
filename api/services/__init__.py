try:
    from services.firestore import firestore_utils
    from services.spotify import spotify_utils
except (ModuleNotFoundError, ImportError):
    from api.services.firestore import firestore_utils
    from api.services.spotify import spotify_utils
