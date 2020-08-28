from PIL import Image

oldimage = Image.open("eiffel.jpg")
# palette = [0, 0, 0, 102, 102, 102, 176, 176, 176, 255, 255, 255]
palette = [0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255]
# palette = [0, 0, 0, 255, 255, 255]

# Generate grayscale palette.
# color_count = 3
# palette = [0, 0, 0]
# for i in range(color_count - 1):
# 	for j in range(3):
# 		palette.append(int(255 / (i + 1)))

# Fill empty spots with zeros, because putpalette expects 256 * 3 ints.
for k in range((256 - int(len(palette) / 3)) * 3):
	palette.append(0)
# print(palette)
# print(len(palette))

palimage = Image.new('P', (16, 16))
# palimage.putpalette(palette * int((256 * 3) / len(palette)))
palimage.putpalette(palette)
newimage = oldimage.quantize(palette=palimage, dither=True)

newimage.show()