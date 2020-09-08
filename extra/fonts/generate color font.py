import os
from PIL import Image
import json

char_size = 8 # all characters are 8x8 in default.png
char_count = 95 # there are 95 characters in ComputerCraft, but note the 64th character ` can't be used later on!
row_count = 6
chars_in_row_max = 16

color_path = 'extra/fonts/color'

if not os.path.exists(color_path):
    os.makedirs(color_path)

with open('extra/fonts/palette.json') as palette:
	colors = json.loads(palette.read())

def get_color(i):
	return (colors[i], colors[i + 1], colors[i + 2])

for row in range(row_count):
	offset = row * chars_in_row_max
	chars_in_row = chars_in_row_max if row < row_count - 1 else chars_in_row_max - 2
	char_img_dimensions = (char_size * chars_in_row, char_size)
	char_img = Image.new('RGB', char_img_dimensions, color = 'black')
	char_pix = char_img.load()

	for char_val in range(chars_in_row):
		i = (row * chars_in_row_max + char_val) * 3
		for bx in range (char_size):
			for by in range (char_size):
				x = char_val * char_size + bx
				y = by
				char_pix[x, y] = get_color(i)

	char_img.save(color_path + '/row ' + str(row + 1) + '.png')
