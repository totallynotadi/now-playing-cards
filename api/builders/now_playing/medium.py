import base64
import re

import requests

from ..utils import build_artist_string, get_text_len


def build_medium_card(track, theme, template):
    image = str(base64.b64encode(track['image'].content))[2: -1]
    template = re.sub(r"{{ image }}", image, template)

    duration = str(int(track['duration_ms'] / 1000))
    template = re.sub(r"{{ duration }}", duration, template)

    animation = "unset"
    if get_text_len(track['name'], 20, 'title') <= 238:
        font_size = "20"
    elif get_text_len(track['name'], 18, 'title') <= 247:
        font_size = "18"
    else:
        animation = "text-scroll infinite linear 20s"
        font_size = "20"
    template = re.sub(r"{{ title_animation }}", animation, template)
    template = re.sub(r"{{ title_font_size }}", font_size, template)
    template = re.sub(r"{{ title }}", track['name'], template)

    animation = "unset"
    font_size = "16"
    artists = build_artist_string(*[artist['name'] for artist in track['artists']])
    if get_text_len(artists, 16, 'artist') >= 242:
        animation = "text-scroll infinite linear 20s"
    template = re.sub(r"{{ artist_animation }}", animation, template)
    template = re.sub(r"{{ artist_font_size }}", font_size, template)
    template = re.sub(r"{{ artist }}", artists, template)

    animation = "unset"
    font_size = "14"
    album = track['album']
    if get_text_len(album['name'], 14, 'subtitle') <= 198:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    elif get_text_len(album['name'], 14, 'subtitle') <= 248:
        subtitle = album['name']
    else:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
        animation = "text-scroll infinite linear 20s"
    template = re.sub(r"{{ sub_animation }}", animation, template)
    template = re.sub(r"{{ sub_font_size }}", font_size, template)
    template = re.sub(r"{{ subtitle }}", subtitle, template)

    template = re.sub(r"{{ bar_color }}", theme['text'].get('bar_color'), template)
    template = re.sub(r"{{ text_color }}", theme['text'].get('text_color'), template, count=4)

    template = re.sub(r"{{ background }}", theme['background'], template)

    return template