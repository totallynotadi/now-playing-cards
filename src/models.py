from dataclasses import dataclass
from typing import Literal, Union

from tests.fireabase_test import FIREBASE_CREDS


@dataclass
class Theme:
    text_color: str = "white"
    background_color: str = "#191414"
    muted_color: str = "#828282"
    border: str = "none"


@dataclass
class CardData:
    image_data: str
    title: str = str()
    artist: str = str()
    album: str = str()
    year: str = str()
    theme: Theme = Theme()


@dataclass
class QueryParams:
    uid: str
    size: Union[Literal["small", "med", "large"], str] = "small"
    theme: Union[Literal["light", "dark", "colorblock", "image"], str] = "dark"
    background_color: str = str()
    text_color: str = str()
