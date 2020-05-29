# import numpy as np
# from scipy.spatial.distance import sqeuclidean as sqdistance
from bisect import bisect_left


## README ####################


# The purpose of this library is to create a dithering effect using only uncolored ComputerCraft (Minecraft) characters.
# This library's get_closest_char() function takes a number between 0 and 1 inclusively, and returns a ComputerCraft character.
# 0 is " " and 1 is "@", and numbers between there get other ComputerCraft characters.
# The characters in the chars table are ordered by the number of cyan 3x3 pixels they are drawn with to accomplish this task.

# This file contains a table with characters in it from Minecraft 1.2.5's character set.
# This is used by the Tekkit Classic modpack's ComputerCraft (1.33) character set.


## VANILLA FONT ####################


# The ordering of this table was done with another python script that has since been deleted.
chars_vanilla = [
	" ", ".", "'", ":", "-", "!", "/", "(", "=", "%",
	"1", "C", "3", "$", "2", "5", "A", "0", "#", "@"
]

char_indices_vanilla = [
	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
	11, 12, 13, 14, 15, 16, 17, 18, 19
]


## 94 GRAYSCALE & COLOR FONT ####################


chars_extended = [
	' ', '!', '\\"', '#', '$', '%', '&', "\\'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'
]

# The program needs this because char 64 has been removed from "chars_extended", because the ` character can't be inserted in ComputerCraft 1.33.
char_indices_extended = [
	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93
]

color_palette = [
	[
		161,
		206,
		143
	],
	[
		240,
		235,
		23
	],
	[
		122,
		54,
		68
	],
	[
		38,
		154,
		210
	],
	[
		122,
		156,
		191
	],
	[
		136,
		235,
		198
	],
	[
		225,
		2,
		170
	],
	[
		246,
		96,
		206
	],
	[
		254,
		124,
		166
	],
	[
		150,
		218,
		99
	],
	[
		203,
		123,
		245
	],
	[
		147,
		119,
		210
	],
	[
		97,
		13,
		187
	],
	[
		216,
		67,
		13
	],
	[
		116,
		79,
		213
	],
	[
		7,
		32,
		189
	],
	[
		65,
		222,
		131
	],
	[
		139,
		72,
		32
	],
	[
		222,
		153,
		166
	],
	[
		29,
		91,
		142
	],
	[
		178,
		3,
		129
	],
	[
		113,
		9,
		3
	],
	[
		171,
		71,
		223
	],
	[
		91,
		111,
		6
	],
	[
		235,
		219,
		143
	],
	[
		68,
		150,
		201
	],
	[
		166,
		72,
		80
	],
	[
		0,
		201,
		125
	],
	[
		123,
		231,
		100
	],
	[
		172,
		160,
		143
	],
	[
		180,
		251,
		94
	],
	[
		9,
		136,
		225
	],
	[
		255,
		46,
		148
	],
	[
		39,
		167,
		41
	],
	[
		70,
		58,
		101
	],
	[
		95,
		146,
		70
	],
	[
		113,
		188,
		33
	],
	[
		31,
		160,
		17
	],
	[
		253,
		182,
		80
	],
	[
		6,
		163,
		213
	],
	[
		12,
		31,
		228
	],
	[
		251,
		230,
		117
	],
	[
		163,
		15,
		228
	],
	[
		22,
		66,
		42
	],
	[
		207,
		64,
		73
	],
	[
		52,
		242,
		7
	],
	[
		50,
		145,
		242
	],
	[
		5,
		71,
		178
	],
	[
		233,
		137,
		46
	],
	[
		185,
		138,
		127
	],
	[
		47,
		37,
		64
	],
	[
		163,
		66,
		1
	],
	[
		104,
		211,
		61
	],
	[
		73,
		86,
		79
	],
	[
		124,
		12,
		201
	],
	[
		127,
		250,
		163
	],
	[
		75,
		67,
		219
	],
	[
		168,
		233,
		104
	],
	[
		104,
		33,
		124
	],
	[
		93,
		91,
		65
	],
	[
		187,
		131,
		182
	],
	[
		210,
		30,
		148
	],
	[
		158,
		124,
		103
	],
	[
		177,
		60,
		169
	],
	[
		191,
		239,
		198
	],
	[
		120,
		144,
		47
	],
	[
		94,
		149,
		40
	],
	[
		97,
		205,
		193
	],
	[
		44,
		51,
		134
	],
	[
		229,
		175,
		56
	],
	[
		170,
		75,
		109
	],
	[
		221,
		33,
		80
	],
	[
		234,
		85,
		225
	],
	[
		76,
		109,
		180
	],
	[
		63,
		220,
		2
	],
	[
		154,
		84,
		46
	],
	[
		218,
		89,
		73
	],
	[
		97,
		131,
		19
	],
	[
		85,
		124,
		111
	],
	[
		94,
		255,
		222
	],
	[
		225,
		31,
		27
	],
	[
		90,
		19,
		33
	],
	[
		145,
		85,
		209
	],
	[
		144,
		222,
		9
	],
	[
		81,
		65,
		47
	],
	[
		241,
		237,
		92
	],
	[
		244,
		66,
		67
	],
	[
		215,
		229,
		56
	],
	[
		211,
		182,
		35
	],
	[
		84,
		168,
		206
	],
	[
		192,
		192,
		89
	],
	[
		219,
		106,
		226
	],
	[
		236,
		92,
		254
	],
	[
		168,
		18,
		17
	]
]

smallest_diff = 282.5


## FUNCTIONS ####################


def get_char(pixel, char_type):
	if char_type == "vanilla" or char_type == "grayscale":	
		return get_closest_char(get_brightness_normal(pixel), char_type)
	elif char_type == "color":
		return get_color_from_palette(pixel)

def get_brightness_normal(tup):
	# Compensates for RGB values not being equally as intense to the human eye.
	brightness = (0.2126 * tup[0] + 0.7152 * tup[1] + 0.0722 * tup[2]) / 255
	if len(tup) == 4:
		return brightness * tup[3] / 255
	else: # TODO: Not sure if necessary.
		return 0


# def find_nearest(array, value):
#     distances = np.asarray([sqdistance(color, value) for color in array])
#     return distances.argmin(axis=0)

# def get_color_from_palette(pixel):
# 	smallestDiffIndex = find_nearest(color_palette, pixel[:3])
# 	return chars_extended[smallestDiffIndex]


def get_color_from_palette(pixel):
	smallest_found_diff = 3 * 255 ** 2 # Init with largest possible diff.
	for i in range(94):
		clr = color_palette[i]
		diff = (pixel[0] - clr[0]) ** 2 + (pixel[1] - clr[1]) ** 2 + (pixel[2] - clr[2]) ** 2
		if diff < smallest_diff: # TODO: Figure out *why* this doesn't seem to speedup the program, even though ~37% of pixels goes here. 
			return chars_extended[i]
		if diff < smallest_found_diff:
			smallest_found_diff = diff
			smallestDiffIndex = i
	return chars_extended[smallestDiffIndex]


def take_closest(indices, my_number):
	""" Assumes myList is sorted. Returns closest value to my_number.
	If two numbers are equally close, return the smallest number. """
	pos = bisect_left(indices, my_number)
	if pos == 0:
		return indices[0]
	if pos == len(indices):
		return indices[-1]
	before = indices[pos - 1]
	after = indices[pos]
	if after - my_number < my_number - before:
		return after
	else:
		return before

# The given n should be between 0 and 1, both inclusive.
def get_closest_char(n, char_type):
	if not (n >= 0 and n <= 1):
		raise ValueError("get_closest_char expected a float between 0 and 1, both inclusive")

	if char_type == "vanilla":
		return chars_vanilla[take_closest(char_indices_vanilla, n * 20)]
	elif char_type == "grayscale":
		return chars_extended[take_closest(char_indices_extended, n * 94)]