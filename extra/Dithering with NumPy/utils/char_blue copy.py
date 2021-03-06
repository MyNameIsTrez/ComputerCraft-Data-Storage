from PIL import Image
import numpy as np


palettes = {
	"color": [0, 0, 0, 0, 0, 255, 0, 255, 0, 0, 255, 255, 255, 0, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 158, 23, 171, 67, 107, 74, 225, 123, 151, 55, 200, 50, 174, 75, 78, 9, 92, 209, 103, 171, 47, 22, 202, 138, 122, 198, 83, 114, 233, 135, 73, 135, 158, 244, 202, 9, 62, 171, 132, 213, 227, 77, 8, 145, 152, 86, 154, 244, 40, 1, 160, 87, 23, 106, 225, 145, 48, 52, 4, 25, 187, 77, 161, 90, 65, 107, 99, 127, 23, 232, 85, 250, 53, 93, 139, 205, 179, 38, 193, 219, 39, 97, 50, 63, 203, 19, 208, 251, 72, 212, 21, 3, 33, 182, 93, 98, 33, 193, 226, 56, 169, 55, 50, 222, 148, 190, 171, 71, 228, 108, 35, 11, 206, 85, 74, 153, 105, 27, 149, 177, 239, 170, 180, 17, 96, 18, 115, 129, 211, 85, 186, 124, 140, 236, 90, 32, 170, 5, 104, 142, 113, 139, 154, 63, 224, 228, 217, 73, 255, 110, 250, 239, 24, 175, 0, 120, 193, 115, 249, 148, 201, 179, 16, 85, 160, 106, 118, 74, 111, 222, 217, 224, 105, 115, 32, 73, 87, 249, 147, 87, 103, 141, 70, 127, 60, 70, 247, 253, 185, 240, 145, 130, 164, 161, 216, 68, 11, 78, 142, 122, 44, 103, 91, 149, 218, 123, 222, 50, 116, 113, 137, 219, 255, 207, 90, 59, 21, 81, 57, 206, 65, 202, 81, 229, 108, 41, 41, 119, 119, 184, 242, 163, 31, 77, 56, 250, 200, 22, 44, 60, 136, 181, 23, 135, 132, 113, 194, 153, 194, 251, 103, 3, 198, 184, 233, 50, 225, 18],
}


chars = {
	"color": [' ', '!', '\\"', '#', '$', '%', '&', "\\'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'],
}


def get_closest_pal(cur_clr, pal, chars_count):
	smallest_dist = float("inf")

	(cur_r, cur_g, cur_b, cur_a) = cur_clr
	# print("cur_r: {}, cur_g: {}, cur_b: {}".format(cur_r, cur_g, cur_b))
	
	for char_idx in range(chars_count):
		# print("\nchar_idx: {}".format(char_idx))

		pal_r = pal[char_idx * 3]
		pal_g = pal[char_idx * 3 + 1]
		pal_b = pal[char_idx * 3 + 2]
		# print("pal_r: {}, pal_g: {}, pal_b: {}".format(pal_r, pal_g, pal_b))

		r_diff = cur_r - pal_r
		g_diff = cur_g - pal_g
		b_diff = cur_b - pal_b
		# print("r_diff: {}, g_diff: {}, b_diff: {}".format(r_diff, g_diff, b_diff))

		avg_r = (cur_r + pal_r) / 2
		# print("avg_r: {}".format(avg_r))

		r_weight = (2 + avg_r / 256) * r_diff ** 2
		g_weight = 4 * g_diff ** 2
		b_weight = (2 + (255 - avg_r) / 256) * b_diff ** 2
		# print("r_weight: {}, g_weight: {}, b_weight: {}".format(r_weight, g_weight, b_weight))

		dist = r_weight + g_weight + b_weight
		# print("dist: {}".format(dist))
		
		if dist < smallest_dist:
			smallest_dist = dist
			closest_char_idx = char_idx
			
			if (len(cur_clr) == 3):
				closest_pal_clr = np.array([pal_r, pal_g, pal_b])
			else:
				closest_pal_clr = np.array([pal_r, pal_g, pal_b, 255])

	return closest_pal_clr, closest_char_idx


def distribute_err(pxls, cur_clr, closest_pal_clr, x, y, w, h):
	err = np.subtract(cur_clr, closest_pal_clr)
	
	add_err(pxls, err, 7, x + 1, y    , w, h)
	add_err(pxls, err, 3, x - 1, y + 1, w, h)
	add_err(pxls, err, 5, x    , y + 1, w, h)
	add_err(pxls, err, 1, x + 1, y + 1, w, h)


def add_err(pxls, err, coeff, x, y, w, h):
	if x < 0 or x >= w or y < 0 or y >= h:
		return
	
	pxls[y, x] = pxls[y, x] + err * coeff / 16


def dither_frame(info):
	modified_width = info["new_width"] - 1

	pal_name = info["palette"]
	pal = palettes[pal_name]
	chars_count = len(chars[pal_name])

	pxls = np.array(info["frame"])

	w = info["frame"].width
	h = info["frame"].height

	dithered_frame = Image.new("RGBA", (modified_width, info["height"]))
	dithered_frame_pxls = np.array(dithered_frame)

	for y in range(info["height"]):
		for x in range(modified_width):
			# print("\n\n\nx :{}, y: {}".format(x, y))

			cur_clr = pxls[y, x]
			# print("cur_clr: {}".format(cur_clr))
			
			closest_pal_clr, char_idx = get_closest_pal(cur_clr, pal, chars_count)
			# print("foo")

			dithered_frame.putpixel((x, y), tuple(closest_pal_clr))

			distribute_err(pxls, cur_clr, closest_pal_clr, x, y, w, h)

	info["dithered_frame"] = dithered_frame
