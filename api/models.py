from dataclasses import dataclass
from typing import Literal, Union


@dataclass
class Theme:
    text_color: str = "white"
    background_color: str = "#191414"


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
