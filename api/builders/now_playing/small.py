import base64
import re

import requests


def build_small_card(track, template):
    image = str(base64.b64encode(requests.get(
        track['album']['images'][1]['url']).content))[2: -1]
    template = re.sub(r"{{ image }}", image, template)

    duration = str(int(track['duration_ms'] / 1000))
    template = re.sub(r"{{ duration }}", duration, template)

    animation = "unset"
    if len(track['name']) <= 16:
        font_size = "18"
    elif len(track['name']) <= 18:
        font_size = "16"
    else:
        font_size = "16"
        animation = "text-scroll infinite linear 20s"
    template = re.sub(r"{{ title_font_size }}", font_size, template)
    template = re.sub(r"{{ title_animation }}", animation, template)
    template = re.sub(r"{{ title }}", track['name'], template)

    animation = "unset"
    artists = ' & '.join([artist['name'] for artist in track['artists']])
    font_size = "14"
    if len(artists) > 23:
        animation = "text-scroll infinite linear 20s"
    template = re.sub(r"{{ artist_font_size }}", font_size, template)
    template = re.sub(r"{{ artist_animation }}", animation, template)
    template = re.sub(r"{{ artist }}", artists, template)

    animation = "unset"
    album = track['album']
    font_size = "12"
    if len(album['name']) <= 13:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    elif len(album['name']) <= 20:
        subtitle = album['name']
    else:
        animation = "text-scroll infinite linear 20s"
    template = re.sub(r"{{ sub_font_size }}", font_size, template)
    template = re.sub(r"{{ sub_animation }}", animation, template)
    template = re.sub(r"{{ subtitle }}", subtitle, template)

    return template