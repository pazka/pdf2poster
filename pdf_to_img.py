# importing required classes
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont
import math
import os
import re
from utils import get_nb_letters_to_print_on_line

PX_IMG_RES = 300
# A0 = 841 x 1189 mm
# IMG_HEIGHT_IN_MM = 1189
# IMG_WIDTH_IN_MM = 841
IMG_HEIGHT = 118 * PX_IMG_RES
IMG_WIDTH = 84 * PX_IMG_RES

CHAR_WIDTH = 4.5
CHAR_HEIGHT = 15

try:
    # remove poster.png
    os.remove('poster.png')
except:
    pass

# creating a pdf reader object
reader = PdfReader('Capital-Volume-I.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

poster = Image.new('RGB', (IMG_WIDTH,
                           IMG_HEIGHT), color=(255, 255, 255))
drawing = ImageDraw.Draw(poster)
font = ImageFont.truetype("arial.ttf", size=12)
position = (0, 0)
text_cursor = 0

# iterate through the pages of pdf file
i = 0
for page in reader.pages:
    print('Page', i)
    i += 1
    # creating an image object
    page_text = page.extract_text()
    normalized_text = re.sub(r'(\n|\r|\\n|\\r)+', '', page_text)
    normalized_text = re.sub(r'(\s|\t)+', ' ', normalized_text)
    normalized_text = re.sub(r'\.+', '.', normalized_text)
    total_nb_letters = len(normalized_text)
    rest_of_text_to_print = normalized_text

    while rest_of_text_to_print != '':

        nb_letter_effectively_printed, length_to_print = get_nb_letters_to_print_on_line(rest_of_text_to_print, position, IMG_WIDTH, font)

        if nb_letter_effectively_printed == 0:
            position = (0, position[1] + CHAR_HEIGHT)
            continue

        printable_text_before_line_return = rest_of_text_to_print[:nb_letter_effectively_printed]

        print(
            f'printing {nb_letter_effectively_printed} letters at {position}')
        drawing.text(position, printable_text_before_line_return,fill=(0, 0, 0),font=font)
        position = (position[0] + length_to_print, position[1])

        rest_of_text_to_print = rest_of_text_to_print[nb_letter_effectively_printed:]

    # saving the image
    poster.save('poster.png')
    print('---')
