try:
    from services.firestore.firestore import firestore_utils
except (ModuleNotFoundError, ImportError):
    from api.services.firestore.firestore import firestore_utils
