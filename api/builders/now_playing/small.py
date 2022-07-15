import base64
import re

import requests

from ..themes import get_theme
from ..utils import get_text_len


def build_small_card(track, background_theme, text_theme, template):
    image = str(base64.b64encode(requests.get(
        track['album']['images'][0]['url']).content))[2: -1]
    template = re.sub(r"{{ image }}", image, template)

    duration = str(int(track['duration_ms'] / 1000))
    template = re.sub(r"{{ duration }}", duration, template)

    animation = "unset"
    if get_text_len(track['name'], 16, 'title') <= 172:
        font_size = "18"
    elif get_text_len(track['name'], 16, 'title') <= 193:
        font_size = "16"
    else:
        font_size = "16"
        animation = "text-scroll infinite linear 16s"
    template = re.sub(r"{{ title_font_size }}", font_size, template)
    template = re.sub(r"{{ title_animation }}", animation, template)
    template = re.sub(r"{{ title }}", track['name'], template)

    animation = "unset"
    artists = ' & '.join([artist['name'] for artist in track['artists']])
    font_size = "14"
    if get_text_len(artists, 14, 'subtitle') > 193:
        animation = "text-scroll infinite linear 16s"
    template = re.sub(r"{{ artist_font_size }}", font_size, template)
    template = re.sub(r"{{ artist_animation }}", animation, template)
    template = re.sub(r"{{ artist }}", artists, template)

    animation = "unset"
    album = track['album']
    font_size = "12"
    if get_text_len(album['name'], 12, 'subtitle') <= 137:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    elif get_text_len(album['name'], 12, 'subtitle') <= 193:
        subtitle = album['name']
    else:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
        animation = "text-scroll infinite linear 16s"
    template = re.sub(r"{{ sub_font_size }}", font_size, template)
    template = re.sub(r"{{ sub_animation }}", animation, template)
    template = re.sub(r"{{ subtitle }}", subtitle, template)

    template = re.sub(r"{{ bar_color }}", text_theme.get('bar_color'), template)
    template = re.sub(r"{{ text_color }}", text_theme.get('text_color'), template, count=4)

    template = re.sub(r"{{ background }}", background_theme, template)

    return template