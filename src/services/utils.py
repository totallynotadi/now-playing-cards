import functools


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance: # type: ignore
            wrapper_singleton.instance = cls(*args, **kwargs) # type: ignore
        return wrapper_singleton.instance # type: ignore

    wrapper_singleton.instance = None # type: ignore
    return wrapper_singleton
