from .small import build_small_card
from .medium import build_medium_card
from .large import build_large_card
from ..themes import *

THEMES = {'dark': text_theme_dark, 'light': text_theme_light}
BACKGROUNDS = {'light': background_light, 'dark': background_dark}

def build(track, template, background_theme, text_theme, size='med'):
    text_theme = THEMES[text_theme]
    if background_theme == 'light':
        text_theme = text_theme_dark
    background_theme = BACKGROUNDS[background_theme]
    if size == 'small':
        return build_small_card(track, background_theme, text_theme, template)
    if size == 'med':
        return build_medium_card(track, background_theme, text_theme, template)
    else:   return build_large_card(track, background_theme, text_theme, template)

