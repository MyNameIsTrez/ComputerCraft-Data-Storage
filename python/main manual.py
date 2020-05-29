import os
import sys
import time
from math import floor
import json

# Utils
import utils.processing as processing


current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))


# USER SETTINGS #######################################


# how to get the extended character set (characters are replaced with grayscale blocks):
# 1. go to %appdata%/.technic/modpacks/tekkit/bin
# 2. remove the minecraft.jar file and replace it with "minecraft.jar versions/new/minecraft.jar",
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
frames_to_update_stats = 1


# string = sys.argv[1]
# print(string)
# files_info = json.loads(string)


# this determines the width and height of the output frames
# see tekkit/config/mod_ComputerCraft.cfg to set custom max_width and max_height values

# (max_width, max_height)
# output_dimensions = (
	# (9, 8), # for single characters, this is 8x8 without the "\n" char at the end
	# (30, 30),
	# (77, 31), # max 8x5 monitor size in ComputerCraft, used because 8x6 doesn't always work
	# (77, 38), # max 8x6 monitor size in ComputerCraft
	# (227, 85), # 1080p
	# (426, 160), # 1440p
	# (640, 240), # 4k
# )

files_info = {
	"data": [
		# {
		# 	"url": "https://uploads.ungrounded.net/alternate/1443000/1443835_alternate_95750.720p.mp4",
		# 	"name": "takeout",
		# 	"extension": "mp4",
		# 	"options": [
		# 		{
		# 			"char_type": "vanilla",
		# 			"width": 10,
		# 			"height": 10
		# 		},
		# 		{
		# 			"char_type": "grayscale",
		# 			"width": 10,
		# 			"height": 10
		# 		},
		# 		{
		# 			"char_type": "color",
		# 			"width": 10,
		# 			"height": 10
		# 		}
		# 	]
		# },
		# {
		# 	"url": "http://uimg.ngfiles.com/icons/7349/7349981_large.png?f1578283262",
		# 	"name": "wavetro logo",
		# 	"extension": "png",
		# 	"options": [
		# 		# {
		# 		# 	"char_type": "grayscale",
		# 		# 	"width": 10,
		# 		# 	"height": 10
		# 		# },
		# 		{
		# 			"char_type": "color",
		# 			"width": 20,
		# 			"height": 20
		# 		},
		# 		{
		# 			"char_type": "color",
		# 			"width": 10,
		# 			"height": 10
		# 		}
		# 	]
		# },
		# {
		# 	"url": "https://mooncatrobot.com/wp-content/uploads/2017/09/emilydevogel_weirdparty.gif",
		# 	"name": "grooving",
		# 	"extension": "gif",
		# 	"options": [
		# 		{
		# 			"char_type": "vanilla",
		# 			"width": 10,
		# 			"height": 10
		# 		}
		# 	]
		# },
		# {
		# 	"url": "https://i.imgur.com/QIY6Pfg.jpg",
		# 	"name": "eiffel",
		# 	"extension": "jpg",
		# 	"options": [
		# 		{
		# 			"char_type": "color",
		# 			"width": 426,
		# 			"height": 160
		# 		}
		# 	]
		# },
		{
			"url": "https://media.giphy.com/media/7GcdjWkek7Apq/giphy.gif",
			"name": "coincidence",
			"extension": "gif",
			"options": [
				# {
				# 	"char_type": "vanilla",
				# 	"width": 426,
				# 	"height": 160
				# },
				# {
				# 	"char_type": "grayscale",
				# 	"width": 426,
				# 	"height": 160
				# },
				{
					"char_type": "color",
					"width": 426,
					"height": 160
				}
			]
		},
		# {
		# 	"url": "https://r3---sn-5hnednlk.googlevideo.com/videoplayback?expire=1590774341&ei=5fXQXpeuONWX1gKq46zgCw&ip=89.98.103.144&id=o-AKavstougk-qMhjv3PfFpMiJGea1tUeQDoVDznROAoKt&itag=22&source=youtube&requiressl=yes&mh=f0&mm=31%2C26&mn=sn-5hnednlk%2Csn-4g5e6nss&ms=au%2Conr&mv=m&mvi=2&pl=16&initcwndbps=1470000&vprv=1&mime=video%2Fmp4&ratebypass=yes&dur=1318.846&lmt=1588441326350002&mt=1590752618&fvip=3&fexp=23882513&c=WEB&txp=5535432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAI1a5okHHDjqWcO9F4I0wRGdHi20AlahYRfisHqLoZ0GAiBu47qOcNqYIOuHZEzYBUl-jjjRrGHHc1dN0wwWBUjK5g%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhANIMZmd5bhJWWWLAV1yxukNqEdu_OI91LQUtC4cH91i0AiEA3WZMXHTKixRCBJkr54X9Uy0_47mV3BjbaE-l50GphAE%3D",
		# 	"name": "lgio satisfactory 9",
		# 	"extension": "mp4",
		# 	"options": [
		# 		# {
		# 		# 	"char_type": "vanilla",
		# 		# 	"width": 426,
		# 		# 	"height": 160
		# 		# },
		# 		{
		# 			"char_type": "color",
		# 			"width": 426,
		# 			"height": 160
		# 		}
		# 	]
		# },
	],
}


# EXECUTION OF THE PROGRAM #######################################


t0 = time.time()

print()

processing.download_files(files_info, current_path)

tempDownloadsPath = os.path.join(current_path, "temp downloads")

print("Processing:")

for file_info in files_info["data"]:
	name = file_info["name"]
	extension = file_info["extension"]
	full_name = os.path.join(name + "." + extension)
	for size in file_info["options"]:
		char_type = size["char_type"]
		max_width = size["width"]
		max_height = size["height"]
		processing.process_frames(name, full_name, max_width, max_height, frame_skipping, char_type, current_path, new_width_stretched, max_bytes_per_file, frames_to_update_stats)

for name in os.listdir(tempDownloadsPath):
	if name != ".empty":
		os.remove(os.path.join(tempDownloadsPath, name))

# Print the time it took to run the program.
time_elapsed = time.time() - t0
minutes = floor(time_elapsed / 60)
seconds = time_elapsed % 60

print("\n\nDone! Duration: {}m, {:.2f}s".format(minutes, seconds))

# sys.stdout.write("\033[F") # Cursor up one line
# sys.stdout.write("\033[K") # Clear to the end of line
# print("Done! Duration: {}m, {:.2f}s".format(minutes, seconds), end="\r", flush=True)