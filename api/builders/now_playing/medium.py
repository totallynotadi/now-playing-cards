import base64
import re

import requests

from ..utils import build_artist_string, get_text_len


def build_medium_card(track, background_theme, text_theme, output):
    image = str(base64.b64encode(requests.get(
        track['album']['images'][0]['url']).content))[2: -1]
    output = re.sub(r"{{ image }}", image, output)

    duration = str(int(track['duration_ms'] / 1000))
    output = re.sub(r"{{ duration }}", duration, output)

    animation = "unset"
    if get_text_len(track['name'], 20, 'title') <= 238:
        font_size = "20"
    elif get_text_len(track['name'], 18, 'title') <= 247:
        font_size = "18"
    else:
        animation = "text-scroll infinite linear 20s"
        font_size = "20"
    output = re.sub(r"{{ title_animation }}", animation, output)
    output = re.sub(r"{{ title_font_size }}", font_size, output)
    output = re.sub(r"{{ title }}", track['name'], output)

    animation = "unset"
    font_size = "16"
    artists = build_artist_string(*[artist['name'] for artist in track['artists']])
    if get_text_len(artists, 16, 'artist') >= 246:
        animation = "text-scroll infinite linear 20s"
    ouptut = re.sub(r"{{ artist_animation }}", animation, output)
    output = re.sub(r"{{ artist_font_size }}", font_size, output)
    output = re.sub(r"{{ artist }}", artists, output)

    animation = "unset"
    font_size = "14"
    album = track['album']
    if get_text_len(album['name'], 14, 'subtitle') <= 198:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    elif get_text_len(album['name'], 14, 'subtitle') <= 246:
        subtitle = album['name']
    else:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
        animation = "text-scroll infinite linear 20s"
    output = re.sub(r"{{ sub_animation }}", animation, output)
    output = re.sub(r"{{ sub_font_size }}", font_size, output)
    output = re.sub(r"{{ subtitle }}", subtitle, output)

    output = re.sub(r"{{ bar_color }}", text_theme.get('bar_color'), output)
    output = re.sub(r"{{ text_color }}", text_theme.get('text_color'), output, count=4)

    output = re.sub(r"{{ background }}", background_theme, output)

    return output