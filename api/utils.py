import io
import json
import math
import os
from typing import Dict
import PIL.Image

import requests
import colorgram
import sty


def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}

def is_light(rgb, threshold=170):
    # https://stackoverflow.com/a/58270890
    [r, g, b] = rgb
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    print(int(hsp))
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



if __name__ == '__main__':
    print(get_image_color({'url': 'https://i.scdn.co/image/ab67616d0000b27356f4dd4f29ddc5f65c70b664'}))
    print()
    print(get_image_color({'url': 'https://i.scdn.co/image/ab67616d0000b273dc04d16605bf254b12743e7c'}))
    print()
    print(get_image_color({'url': 'https://i.scdn.co/image/ab67616d0000b273c5716278abba6a103ad13aa7'}))


