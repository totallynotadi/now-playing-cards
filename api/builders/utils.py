import io
import math
from typing import Dict, Literal, Tuple
from copy import deepcopy
import string

import colorgram
import PIL.Image
import requests
from PIL import ImageFont

from .themes import *


FONT_SIZES = {
    'title': 'api/builders/fonts/inter-500.ttf',
    'artist': 'api/builders/fonts/inter-600.ttf',
    'subtitle': 'api/builders/fonts/inter-500.ttf'
}


def get_text_len(text: str, font_size: int, font_name: Literal['title', 'artist', 'subtitle']) -> int:
    font = ImageFont.truetype(FONT_SIZES[font_name], font_size)
    size = font.getlength(str(text))
    return int(size)


def build_artist_string(*args):
    artists = list(args)
    if len(artists) > 2:
        res = ', '.join(list(artists)[:-1])
        res += ' & ' + artists[-1]
    elif len(artists) == 2:
        res = ' & '.join(artists)
    else:
        res = artists[0]
    return res


def is_light(rgb, threshold=168):
    # https://stackoverflow.com/a/58270890
    [r, g, b] = rgb
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    return hsp > threshold


def rgb_to_hex(rgb):
    return '#' + ('%02x%02x%02x' % rgb)


def get_image_color(image: requests.Response) -> Tuple[str, ...]:
    image = image.content
    image = PIL.Image.open(io.BytesIO((image)))
    
    # so that color extraction takes less time.
    small_image = image.resize((size // 4 for size in image.size))

    colors = colorgram.extract(small_image, 5)
    color = tuple(colors[0].rgb)

    return color


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
        'rgb' not in color_code and
        check_contains_digit(color_code) and
        check_contains_char(color_code)
    ):
        return '#' + str(color_code)
    return color_code


def parse_params(params):
    size = params.get('size', 'med')
    theme = params.get('theme', 'dark')
    bar = params.get('bar', 'progress-bar')

    card_theme = deepcopy(THEMES[theme])
    bar_theme = deepcopy(BARS[bar])

    text_color = params.get('text-color', card_theme['text']['text_color'])
    background_color = params.get('bg-color', card_theme['background'])

    card_theme['text']['text_color'] = check_color_integer(text_color)
    card_theme['background'] = check_color_integer(background_color)
    card_theme['bar'] = bar_theme

    if size not in ['default', 'small', 'med', 'large']:
        size = 'med'
    elif size in 'default':
        size = 'med'

    with open(f'api/cards/card_{size}.svg', 'r', encoding='utf-8') as file:
        card_template = str(file.read())

    return card_theme, card_template, size


if __name__ == "__main__":
    # print(get_text_len('W.A.V.E (Bonus Tracioi', 16, 'title'))

    print(get_image_color(
        {'url': 'https://i.scdn.co/image/ab67616d0000b27356f4dd4f29ddc5f65c70b664'}), end='\n')
    print(get_image_color(
        {'url': 'https://i.scdn.co/image/ab67616d0000b273dc04d16605bf254b12743e7c'}), end='\n')
    print(get_image_color(
        {'url': 'https://i.scdn.co/image/ab67616d0000b273c5716278abba6a103ad13aa7'}), end='\n')
