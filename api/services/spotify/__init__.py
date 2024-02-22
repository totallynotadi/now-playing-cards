try:
    from services.spotify.spotify import spotify_utils
except (ModuleNotFoundError, ImportError):
    from api.services.spotify.spotify import spotify_utils
