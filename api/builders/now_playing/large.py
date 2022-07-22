import base64
import re

import requests

from ..utils import get_text_len


def build_large_card(track, background_theme, text_theme, output):
    image = str(base64.b64encode(requests.get(
        track['album']['images'][0]['url']).content))[2: -1]
    output = re.sub(r"{{ image }}", image, output)

    duration = str(int(track['duration_ms'] / 1000))
    output = re.sub(r"{{ duration }}", duration, output)

    animation = "unset"
    font_size = "20"
    artist_top_margin = "8"
    title = track['name']
    if get_text_len(title, 20, 'title') <= 274:
        font_size = "20"
    elif get_text_len(title, 18, 'title') <= 271:
        font_size = "18"
    elif get_text_len(title, 16, 'title') <= 274:
        font_size = "16"
        artist_top_margin = "6"
    output = re.sub(r"{{ artist_top_margin }}", artist_top_margin, output)
    output = re.sub(r"{{ title_font_size }}", font_size, output)
    output = re.sub(r"{{ title }}", title, output)

    artists = ' & '.join([artist['name'] for artist in track['artists']])
    output = re.sub(r"{{ artist }}", artists, output)

    album = track['album']
    subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    output = re.sub(r"{{ subtitle }}", subtitle, output)

    output = re.sub(r"{{ bar_color }}", text_theme.get('bar_color'), output)
    output = re.sub(r"{{ text_color }}", text_theme.get('text_color'), output, count=6)

    output = re.sub(r"{{ background }}", background_theme, output)

    return output