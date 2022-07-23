from .small import build_small_card
from .medium import build_medium_card
from .large import build_large_card
from ..themes import *


SIZES = {'large': build_large_card, 'default': build_medium_card, 'med': build_medium_card, 'small': build_small_card}

def build(track, theme, template, size='med'):
    func = SIZES[size]
    return func(track, theme, template)
