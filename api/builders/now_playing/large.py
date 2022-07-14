import base64
import re

import requests


def build_large_card(track, output):
    image = str(base64.b64encode(requests.get(
        track['album']['images'][1]['url']).content))[2: -1]
    output = re.sub(r"{{ image }}", image, output)

    duration = str(int(track['duration_ms'] / 1000))
    output = re.sub(r"{{ duration }}", duration, output)

    output = re.sub(r"{{ title }}", track['name'], output)

    artists = ' & '.join([artist['name'] for artist in track['artists']])
    output = re.sub(r"{{ artist }}", artists, output)

    album = track['album']
    subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    output = re.sub(r"{{ subtitle }}", subtitle, output)

    return output