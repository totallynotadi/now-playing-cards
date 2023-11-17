import base64
import math
import string
from typing import Dict, List

import themes
import vibrant
from models import CardData, QueryParams, Theme

V = vibrant.Vibrant()


def build_artist_string(*args) -> str:
    artists = list(args)
    if len(artists) > 2:
        res = ", ".join(list(artists)[:-1])
        res += " & " + artists[-1]
    elif len(artists) == 2:
        res = " & ".join(artists)
    else:
        res = artists[0]
    return res


def is_light(rgb: List[int], threshold: int = 168) -> bool:
    # https://stackoverflow.com/a/58270890
    r, g, b = rgb
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    return hsp > threshold


def rgb_to_hex(rgb) -> str:
    return "#" + ("%02x%02x%02x" % tuple(rgb))


def get_image_color(image: bytes) -> vibrant.Palette:
    return V.get_palette(image)


def check_contains_digit(color: str) -> bool:
    for digit in string.digits:
        if digit in color:
            return True
    return False


def check_contains_char(color: str) -> bool:
    for char in string.ascii_letters:
        if char in color:
            return True
    return False


def check_color_integer(color_code: str) -> str:
    if (
        "rgb" not in color_code
        and check_contains_digit(color_code)
        and check_contains_char(color_code)
    ):
        return "#" + str(color_code)
    return color_code


def resolve_theme(theme: str, image: bytes) -> Theme:
    final_theme = themes.THEMES[theme]
    if theme != "extract" and theme != "image":
        return final_theme
    elif theme == "extract":
        print("::: image type - ", type(image))
        color = get_image_color(image).muted.rgb

        final_theme.background_color = rgb_to_hex(color)
        final_theme.text_color = (
            themes.text_color_dark if is_light(color) else themes.text_color_light
        )
    elif theme == "image":
        ...
    elif theme == "gradient":
        ...
    return final_theme


def parse_params(params: QueryParams, track: Dict) -> CardData:
    image = track["image"]
    title = track["name"]
    artist = build_artist_string(
        *[artist["name"] for artist in track["artists"]],
    )
    album = track["album"]["name"]
    year = track["album"]["release_date"].split("-")[0]
    theme = resolve_theme(params.theme, image)

    image = str(base64.b64encode(image))[2:-1]
    return CardData(
        image_data=image,
        title=title,
        artist=artist,
        album=album,
        year=year,
        theme=theme,
    )
