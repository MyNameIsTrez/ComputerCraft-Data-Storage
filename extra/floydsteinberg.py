from PIL import Image

oldimage = Image.open("eiffel.jpg")
palette = [0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255]
# palette = [0, 0, 0, 102, 102, 102, 176, 176, 176, 255, 255, 255]
# palette = [0, 0, 0, 255, 255, 255]

# Fill empty spots with zeros, because putpalette expects 256 * 3 ints.
for k in range((256 - int(len(palette) / 3)) * 3):
	palette.append(0)

palette_img = Image.new('P', (16, 16))
# palette_img.putpalette(palette * int((256 * 3) / len(palette)))
palette_img.putpalette(palette)

# TODO: Time if it's faster to use getpalette() instead of adding .convert('RGB'):
# https://stackoverflow.com/a/59724281/13279557
newimage = oldimage.quantize(palette=palette_img, dither=True)

# palette = newimage.getpalette()
for i in range(2):
	for j in range(2):
		index = newimage.getpixel((i, j))  # index in the palette
		print(index)
		# base = 3 * index  # because each palette color has 3 components
		# r, g, b = palette[base:base+3]
		# print("r: {}, g: {}, b: {}".format(r, g, b))

# # newimage.show()


# color_count = 20
# for i in range(color_count):
# 	c = round(255 / (color_count - 1) * i)
# 	print("{}, {}, {}, ".format(c, c, c), end="")