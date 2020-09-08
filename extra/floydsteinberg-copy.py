from PIL import Image

old_img = Image.open("eiffel.jpg")
scale = 1
print((int(old_img.width * scale), int(old_img.height * scale)))
old_img = old_img.resize((int(old_img.width * scale), int(old_img.height * scale)))

palette = [161,206,143,240,235,23,122,54,68,38,154,210,122,156,191,136,235,198,225,2,170,246,96,206]
# palette = [127, 127, 127, 255, 255, 255]
# palette = [0, 0, 0, 255, 255, 255]

# putpalette() always expects 256 * 3 ints.
for k in range(256 - int(len(palette) / 3)):
	for j in range(3):
		palette.append(palette[j])

palette_img = Image.new('P', (1, 1))
palette_img.putpalette(palette)
new_img = old_img.quantize(palette=palette_img, dither=True)
new_img.show()