try:
    from models import Theme
except Exception:
    from .models import Theme

text_color_dark = "rgba(96, 95, 95, 1)"
text_color_light = "white"

background_dark = "#191414"
background_light = "rgba(229, 229, 229, 1)"

theme_light = Theme(text_color_dark, background_light)
theme_dark = Theme(text_color_light, background_dark)

THEMES = {
    "default": theme_dark,
    "light": theme_light,
    "dark": theme_dark,
    "extract": Theme(),
    "image": Theme(),
}
