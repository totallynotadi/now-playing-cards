text_theme_dark = {'bar_color': 'rgba(147, 147, 147, 1)', 'text_color': 'rgba(96, 95, 95, 1)'}
text_theme_light = {'bar_color': 'rgba(188, 188, 188, 1)', 'text_color': 'white'}

# background_dark = 'rgba(40, 64, 102, 1)'
background_dark = 'rgba(53, 71, 99, 1)'
background_light = 'rgba(229, 229, 229, 1)'

theme_light = {'text': text_theme_dark, 'background': background_light}
theme_dark = {'text': text_theme_light, 'background': background_dark}
theme_colorblock = {'text': text_theme_light, 'background': 'extract'}
theme_gradient = {'text': text_theme_light, 'background': 'gradient'}
theme_image = {'text': text_theme_light, 'background': 'blur'}

THEMES = {'light': theme_light, 'dark': theme_dark, 'colorblock': theme_colorblock, 'image': theme_image}

def get_theme(image):
    pass
