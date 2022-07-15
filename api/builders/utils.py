from PIL import ImageFont


SIZES = {'title': 'builders/fonts/inter-700.ttf', 'artist': 'builders/fonts/inter-600.ttf', 'subtitle': 'builders/fonts/inter-500.ttf'}

def get_text_len(text, font_size, font_name):
    font = ImageFont.truetype(SIZES[font_name], font_size)
    size = font.getsize(text)
    return size[0]


if __name__ == "__main__":
    print(get_text_len('W.A.V.E (Bonus Tracioi', 16, 'title'))