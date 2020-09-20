from PIL import Image
import numpy as np


palettes = {
	"vanilla": [0, 0, 0, 13, 13, 13, 27, 27, 27, 40, 40, 40, 54, 54, 54, 67, 67, 67, 81, 81, 81, 94, 94, 94, 107, 107, 107, 121, 121, 121, 134, 134, 134, 148, 148, 148, 161, 161, 161, 174, 174, 174, 188, 188, 188, 201, 201, 201, 215, 215, 215, 228, 228, 228, 242, 242, 242, 255, 255, 255],

	"color": [0, 0, 0, 0, 0, 255, 0, 255, 0, 0, 255, 255, 255, 0, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 158, 23, 171, 67, 107, 74, 225, 123, 151, 55, 200, 50, 174, 75, 78, 9, 92, 209, 103, 171, 47, 22, 202, 138, 122, 198, 83, 114, 233, 135, 73, 135, 158, 244, 202, 9, 62, 171, 132, 213, 227, 77, 8, 145, 152, 86, 154, 244, 40, 1, 160, 87, 23, 106, 225, 145, 48, 52, 4, 25, 187, 77, 161, 90, 65, 107, 99, 127, 23, 232, 85, 250, 53, 93, 139, 205, 179, 38, 193, 219, 39, 97, 50, 63, 203, 19, 208, 251, 72, 212, 21, 3, 33, 182, 93, 98, 33, 193, 226, 56, 169, 55, 50, 222, 148, 190, 171, 71, 228, 108, 35, 11, 206, 85, 74, 153, 105, 27, 149, 177, 239, 170, 180, 17, 96, 18, 115, 129, 211, 85, 186, 124, 140, 236, 90, 32, 170, 5, 104, 142, 113, 139, 154, 63, 224, 228, 217, 73, 255, 110, 250, 239, 24, 175, 0, 120, 193, 115, 249, 148, 201, 179, 16, 85, 160, 106, 118, 74, 111, 222, 217, 224, 105, 115, 32, 73, 87, 249, 147, 87, 103, 141, 70, 127, 60, 70, 247, 253, 185, 240, 145, 130, 164, 161, 216, 68, 11, 78, 142, 122, 44, 103, 91, 149, 218, 123, 222, 50, 116, 113, 137, 219, 255, 207, 90, 59, 21, 81, 57, 206, 65, 202, 81, 229, 108, 41, 41, 119, 119, 184, 242, 163, 31, 77, 56, 250, 200, 22, 44, 60, 136, 181, 23, 135, 132, 113, 194, 153, 194, 251, 103, 3, 198, 184, 233, 50, 225, 18],
}


chars = {
	"vanilla": [" ", ".", "'", ":", "-", "!", "/", "(", "=", "%", "1", "C", "3", "$", "2", "5", "A", "0", "#", "@"],

	"color": [' ', '!', '\\"', '#', '$', '%', '&', "\\'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'],
}


def get_idx(x, y, w):
	return x + y * w


def get_clr(pxls, x, y, w):
	i = get_idx(x, y, w)
	return pxls[i]


def get_closest_pal(cur_clr, pal, chars_count):
	smallest_dist = float("inf")

	cur_r = cur_clr[0]
	cur_g = cur_clr[1]
	cur_b = cur_clr[2]
	
	for char_idx in range(chars_count):
		pal_r = pal[char_idx * 3 + 0]
		pal_g = pal[char_idx * 3 + 1]
		pal_b = pal[char_idx * 3 + 2]
		
		diff_r = (cur_r - pal_r) ** 2
		diff_g = (cur_g - pal_g) ** 2
		diff_b = (cur_b - pal_b) ** 2

		dist = diff_r + diff_g + diff_b
		
		if dist < smallest_dist:
			smallest_dist = dist
			closest_pal_clr = (pal_r, pal_g, pal_b)
			closest_char_idx = char_idx

	# closest_pal_clr = (pal[0], pal[1], pal[2])
	# closest_char_idx = 0

	return closest_pal_clr, closest_char_idx


def set_clr(pxls, clr, x, y, w):
	i = get_idx(x, y, w)
	pxls[i] = clr


def distribute_err(pxls, cur_clr, closest_pal_clr, x, y, w, h):
	# TODO: This can just be a - when closest_pal_clr is a np array
	err = np.subtract(cur_clr, closest_pal_clr)
	
	add_err(pxls, err, 7, x + 1, y    , w, h)
	add_err(pxls, err, 3, x - 1, y + 1, w, h)
	add_err(pxls, err, 5, x    , y + 1, w, h)
	add_err(pxls, err, 1, x + 1, y + 1, w, h)

def add_err(pxls, err, coeff, x, y, w, h):
	# TODO: x >= w and y >= h may cause bugs
	if x < 0 or x >= w or y < 0 or y >= h:
		return
	
	cur_clr = get_clr(pxls, x, y, w)
	new_clr = cur_clr + err * coeff / 16
	set_clr(pxls, new_clr, x, y, w)


def get_char(pal_name, char_idx):
	return chars[pal_name][char_idx]


# TODO: Increase speed with pxls as a NP array, look up "python pil replace a single rgba color" on StackOverflow for it
def dither_to_str(info):
	# TODO: Compare performance with a list, because Python may be recreating the string after every +=
	string = ""

	# the \n character at the end of every line needs to have one spot reserved
	# TODO: do the -1 at the resizing of the frame instead
	# Is it really necessary to use ["new_width"] instead of ["frame"].width?
	modified_width = info["new_width"] - 1

	pal_name = info["palette"]
	pal = palettes[pal_name]
	chars_count = len(chars[pal_name])

	# TODO: Try to remove the list() call
	# pxls = list(info["frame"].getdata())
	# TODO: np.array call seems pretty slow with 0.08s as opposed to 0.01s with list()
	pxls = np.array(info["frame"].getdata())

	w = info["frame"].width
	h = info["frame"].height

	for y in range(info["height"]):
		for x in range(modified_width): #TODO: modified_width be gone
			cur_clr = get_clr(pxls, x, y, w)

			# This function is extremely slow for some reason
			closest_pal_clr, char_idx = get_closest_pal(cur_clr, pal, chars_count)
			
			# string += get_char(pal_name, char_idx)
			
			# distribute_err(pxls, cur_clr, closest_pal_clr, x, y, w, h)
		
		# TODO: why not y < h - 1?
		if y < info["height"] - 1:
			# add a return character to the end of each horizontal line,
			# so ComputerCraft can draw the entire frame with one write() statement
			string += "\\n"
	return string
