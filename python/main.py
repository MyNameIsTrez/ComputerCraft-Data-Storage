import os
import sys
import time
from math import floor
import json

# Temporary way to access the dithering lib. Refactor later.
currentPath = os.path.join(os.path.dirname(os.path.abspath(__file__)))

import utils.processing as processing


# USER SETTINGS #######################################


# default is False
# if true, the program assumes 94 characters are available, instead of the usual 20
# 94 are available by replacing Tekkit's default characters in default.png, see the instructions below
extended_chars = False

# how to get the extended character set (characters are replaced with grayscale blocks):
# 1. go to %appdata%/.technic/modpacks/tekkit/bin
# 2. remove the minecraft.jar file and replace it with 'minecraft.jar versions/new/minecraft.jar',
#    which can be found inside the same folder of this program
# 3. tekkit's characters should now all be replaced with 94 grayscale colors, instead of the default 19
# 4. when you want to go back to the default font,
# 	 replace the new minecraft.jar file with 'minecraft.jar versions/old/minecraft.jar'

# if true, the original aspect ratio won't be kept so the width can be stretched to max_width
new_width_stretched = True

# a file compression method
# 1 means every frame of the video is kept, 3 means every third frame of the video is kept
frame_skipping = 1

# 100 MB GitHub file limit. 9.5e7 is 95 million.
max_bytes_per_file = 9.5e7

# how many frames have to be processed before the stats in the console are updated
frames_to_update_stats = 100


# string = sys.argv[1]
# print(string)
# files_info = json.loads(string)


# this determines the width and height of the output frames
# see tekkit/config/mod_ComputerCraft.cfg to set your own max_width and max_height values

# (max_width, max_height)
# output_dimensions = (
	# (9, 8), # for single characters, this is 8x8 without the '\n' char at the end
	# (30, 30),
	# (77, 31), # max 8x5 monitor size in ComputerCraft, used because 8x6 doesn't always work
	# (77, 38), # max 8x6 monitor size in ComputerCraft
	# (227, 85), # 1080p
	# (426, 160), # 1440p
	# (640, 240), # 4k
# )

files_info = {
	'data': [
		# {
		# 	'url': 'https://uploads.ungrounded.net/alternate/1443000/1443835_alternate_95750.720p.mp4',
		# 	'name': 'takeout',
		# 	'extension': 'mp4',
		# 	'width': 30,
		# 	'height': 30
		# },
		{
			'url': 'http://uimg.ngfiles.com/icons/7349/7349981_large.png?f1578283262',
			'name': 'wavetro logo',
			'extension': 'png',
			'width': 30,
			'height': 30
		},
		# {
		# 	'url': 'https://mooncatrobot.com/wp-content/uploads/2017/09/emilydevogel_weirdparty.gif',
		# 	'name': 'grooving',
		# 	'extension': 'gif',
		# 	'width': 30,
		# 	'height': 30
		# }
	],
}


# EXECUTION OF THE PROGRAM #######################################


print()

t0 = time.time()

processing.download_files(files_info, currentPath)

tempDownloadsPath = os.path.join(currentPath, 'temp downloads')

# for dimension in output_dimensions:
	# max_width, max_height = dimension
	# for name in os.listdir(tempDownloadsPath):
		# if name != '.empty': # '.empty' prevents the folder from being removed on GitHub
	# print()

for file_info in files_info['data']:
	name = file_info['name']
	extension = file_info['extension']
	full_name = os.path.join(name + '.' + extension)

	max_width = file_info['width']
	max_height = file_info['height']

	processing.process_frames(full_name, max_width, max_height, frame_skipping, extended_chars, currentPath, new_width_stretched, max_bytes_per_file, frames_to_update_stats)

for name in os.listdir(tempDownloadsPath):
	if name != '.empty':
		os.remove(os.path.join(tempDownloadsPath, name))

# print the time it took to run the program
time_elapsed = time.time() - t0
minutes = floor(time_elapsed / 60)
seconds = time_elapsed % 60

print('Done! Duration: {}m, {:.2f}s'.format(minutes, seconds))

# sys.stdout.write("\033[F") # Cursor up one line
# sys.stdout.write("\033[K") # Clear to the end of line
# print('Done! Duration: {}m, {:.2f}s'.format(minutes, seconds), end='\r', flush=True)