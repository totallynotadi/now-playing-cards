import base64
import re

import requests


def build_large_card(track, background_theme, text_theme, output):
    image = str(base64.b64encode(requests.get(
        track['album']['images'][0]['url']).content))[2: -1]
    output = re.sub(r"{{ image }}", image, output)

    duration = str(int(track['duration_ms'] / 1000))
    output = re.sub(r"{{ duration }}", duration, output)

    output = re.sub(r"{{ title }}", track['name'], output)

    artists = ' & '.join([artist['name'] for artist in track['artists']])
    output = re.sub(r"{{ artist }}", artists, output)

    album = track['album']
    subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    output = re.sub(r"{{ subtitle }}", subtitle, output)

    output = re.sub(r"{{ bar_color }}", text_theme.get('bar_color'), output)
    output = re.sub(r"{{ text_color }}", text_theme.get('text_color'), output, count=6)

    output = re.sub(r"{{ background }}", background_theme, output)

    return output