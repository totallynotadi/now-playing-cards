import io
import math
from typing import Dict, Literal
from copy import deepcopy

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
    size = font.getsize(text)
    return size[0]


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


def is_light(rgb, threshold=170):
    # https://stackoverflow.com/a/58270890
    [r, g, b] = rgb
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    return hsp > threshold


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def get_image_color(image: Dict) -> str:
    image = requests.get(image['url']).content
    image = PIL.Image.open(io.BytesIO((image)))

    small_image = image.resize((size // 4 for size in image.size))

    colors = colorgram.extract(small_image, 5)
    color = tuple(colors[0].rgb)
    # print(color)

    # small_image_colors, pixel_count = extcolors.extract_from_image(
    #     small_image, tolerance=28, limit=5)

    # for color in small_image_colors:
    #     color = color[0]
    #     print(sty.bg(color[0], color[1], color[2]) + "    " + sty.bg.rs)
    # return rgb_to_hex((small_image_colors[0][0]))

    # print(is_light(color))
    # print(sty.bg(color[0], color[1], color[2]) + "    " + sty.bg.rs)

    return rgb_to_hex(color)


def check_color_integer(color_code):
    print(f':::{color_code}')
    try:
        color_int = int(color_code)
        print(f'::::{str(color_code)}')
        return '#' + str(color_code)
    except Exception as e:
        print(e)
        return color_code


def parse_params(params):
    size = params.get('size', 'med')
    theme = params.get('theme', 'dark')
    card_theme = deepcopy(THEMES[theme])

    text_color = params.get('text-color', card_theme['text']['text_color'])
    background_color = params.get('bg-color', card_theme['background'])

    card_theme['text']['text_color'] = check_color_integer(text_color)
    card_theme['background'] = check_color_integer(background_color)

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
