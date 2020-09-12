from PIL import Image
import numpy as np

palettes = {
	"vanilla": [0, 0, 0, 13, 13, 13, 27, 27, 27, 40, 40, 40, 54, 54, 54, 67, 67, 67, 81, 81, 81, 94, 94, 94, 107, 107, 107, 121, 121, 121, 134, 134, 134, 148, 148, 148, 161, 161, 161, 174, 174, 174, 188, 188, 188, 201, 201, 201, 215, 215, 215, 228, 228, 228, 242, 242, 242, 255, 255, 255],

	"color": [0,0,0,0,0,255,0,255,0,0,255,255,255,0,0,255,0,255,255,255,0,255,255,255,212,62,232,113,46,66,57,223,57,32,102,95,236,205,145,185,226,216,231,185,42,196,112,129,48,142,226,235,4,59,9,216,122,241,74,168,51,131,135,109,163,238,204,143,187,94,72,157,54,47,87,96,244,199,225,36,85,196,15,89,255,24,50,121,10,124,33,61,255,169,170,162,151,119,50,82,213,122,240,11,170,71,108,158,14,77,194,99,17,209,189,17,233,239,138,243,107,172,49,106,85,219,12,236,82,62,62,39,185,46,51,99,117,159,1,131,236,195,231,254,148,164,15,125,147,153,113,254,69,162,104,154,125,116,134,208,179,197,247,108,243,42,207,105,201,208,236,182,147,211,180,39,119,195,164,10,92,21,8,162,183,112,60,53,229,195,5,152,136,252,4,123,39,211,228,240,163,209,166,54,164,90,93,28,29,1,38,122,23,47,28,206,159,88,3,132,27,8,28,163,5,32,31,44,243,3,28,150,212,195,204,121,29,41,149,59,43,187,181,66,234,209,16,138,41,20,14,69,28,43,232,33,75,7,77,63,11,106,213,223,45,162,88,74,203,237,133,246,169,58,56,147,11,73,29,53,93,44],

	"lmao": [0,0,0,255,255,255,255,0,0]
}

chars = {
	"vanilla": [" ", ".", "'", ":", "-", "!", "/", "(", "=", "%", "1", "C", "3", "$", "2", "5", "A", "0", "#", "@"],

	"color": [' ', '!', '\\"', '#', '$', '%', '&', "\\'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'],

	"lmao": [" ", "\\'", "$"]
}


def get_idx(x, y, w):
	return x + y * w


def get_clr(pxls, x, y, w):
	i = get_idx(x, y, w)
	return pxls[i]


def get_closest_pal(cur_clr, pal, chars_count):
	smallest_dist = float("inf")
	
	for char_idx in range(chars_count):
		pal_r = pal[char_idx * 3 + 0]
		pal_g = pal[char_idx * 3 + 1]
		pal_b = pal[char_idx * 3 + 2]
		
		diff_r = (cur_clr[0] - pal_r) ** 2
		diff_g = (cur_clr[1] - pal_g) ** 2
		diff_b = (cur_clr[2] - pal_b) ** 2

		dist = diff_r + diff_g + diff_b
		
		if dist < smallest_dist:
			smallest_dist = dist
			closest_pal_clr = (pal_r, pal_g, pal_b)
			closest_char_idx = char_idx

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

			closest_pal_clr, char_idx = get_closest_pal(cur_clr, pal, chars_count)
			
			string += get_char(pal_name, char_idx)
			
			distribute_err(pxls, cur_clr, closest_pal_clr, x, y, w, h)
		
		# TODO: why not y < h - 1?
		if y < info["height"] - 1:
			# add a return character to the end of each horizontal line,
			# so ComputerCraft can draw the entire frame with one write() statement
			string += "\\n"
	return string
