import base64
import re

import requests

from ..utils import get_text_len, build_artist_string


def build_large_card(track, theme, template):
    image = str(base64.b64encode(track['image'].content))[2: -1]
    template = re.sub(r"{{ image }}", image, template)

    duration = str(int(track['duration_ms'] / 1000))
    template = re.sub(r"{{ duration }}", duration, template)

    bar_type = theme['bar'].get('bar_type', 'progress-bar')
    template = re.sub(r"{{ bar_type }}", bar_type, template)

    bar_data = theme['bar'].get('bar_data', '<div class="meter"></div>')
    template = re.sub(r"{{ bar_data }}", bar_data, template)

    animation = "unset"
    font_size = "20"
    artist_top_margin = "8"
    title = track['name']
    if get_text_len(title, 20, 'title') <= 276:
        font_size = "20"
    elif get_text_len(title, 18, 'title') <= 273:
        font_size = "18"
    elif get_text_len(title, 16, 'title') <= 278:
        font_size = "16"
    else:
        font_size = "16"
        artist_top_margin = "6"
        animation = "text-scroll infinite linear 20s"
    # artist top margin being set here in title section because the top margin depends upon the size of the title
    template = re.sub(r"{{ title }}", title, template)
    template = re.sub(r"{{ title_font_size }}", font_size, template)
    template = re.sub(r"{{ title_animation }}", animation, template)
    template = re.sub(r"{{ artist_top_margin }}", artist_top_margin, template)

    animation = "unset"
    artists = build_artist_string(*[artist['name']for artist in track['artists']])
    if get_text_len(artists, 14, 'artist') >= 278:
        animation = "text-scroll infinite linear 20s"
    template = re.sub(r"{{ artist_animation }}", animation, template)
    template = re.sub(r"{{ artist }}", artists, template)

    animation = "unset"
    album = track['album']
    if get_text_len(album['name'], 14, 'subtitle') <= 228:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
    elif get_text_len(album['name'], 14, 'subtitle') <= 275:
        subtitle = album['name']
    else:
        subtitle = album['name'] + ' • ' + album['release_date'].split('-')[0]
        animation = "text-scroll infinite linear 20s"
    template = re.sub(r"{{ subtitle }}", subtitle, template)
    template = re.sub(r"{{ subtitle_animation }}", animation, template)

    template = re.sub(r"{{ bar_color }}",
                      theme['text'].get('bar_color'), template)
    template = re.sub(r"{{ text_color }}", theme['text'].get(
        'text_color'), template, count=7)

    template = re.sub(r"{{ background }}", theme['background'], template)

    return template
