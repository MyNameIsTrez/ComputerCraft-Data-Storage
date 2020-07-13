import os, sys, time, json
from math import floor

# From the utils folder
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


# EXECUTION OF THE PROGRAM #######################################


files_info = json.loads(sys.argv[1])
print(files_info, files_info[0]["id"])

t0 = time.time()

print("Downloading URL files:")
temp_downloads_path = os.path.join(current_path, "temp downloads")
processing.download_url_files(files_info, temp_downloads_path)

print("\nProcessing:")
for file_info in files_info:
	url_name = file_info["url_name"]
	extension = file_info["extension"]
	url_file_path = os.path.join(temp_downloads_path, url_name + "." + extension)
	for variation in file_info["variations"]:
		palette = variation["palette"]
		max_width = variation["width"]
		max_height = variation["height"]
		processing.process_frames(url_name, extension, url_file_path, max_width, max_height, frame_skipping, palette, current_path, new_width_stretched, max_bytes_per_file, frames_to_update_stats)

processing.remove_url_files(temp_downloads_path)

# Print the time it took to run the program.
time_elapsed = time.time() - t0
minutes = floor(time_elapsed / 60)
seconds = time_elapsed % 60
print("\n\nDone! Duration: {}m, {:.2f}s".format(minutes, seconds))

# sys.stdout.write("\033[F") # Cursor up one line
# sys.stdout.write("\033[K") # Clear to the end of line
# print("Done! Duration: {}m, {:.2f}s".format(minutes, seconds), end="\r", flush=True)