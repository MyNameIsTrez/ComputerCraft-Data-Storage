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

# if true, print a minimal amount of live statistics for each file
minimal_printing = False

# if true, the original aspect ratio won't be kept so the width can be stretched to max_width
new_width_stretched = True

# a file compression method
# 1 means every frame of the video is kept, 3 means every third frame of the video is kept
frame_skipping = 1

# 100 MB GitHub file limit. 9.5e7 is 95 million
max_bytes_per_file = 9.5e7

# how many frames have to be processed before the stats in the console are updated
frames_to_update_stats = 1


# EXECUTION OF THE PROGRAM #######################################


# read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    # since the input would only be having one line, parse the JSON data from that
    return json.loads(lines[0])

def main():
	try:
		entries = read_in()

		t0 = time.time()

		print("\nDownloading URL files", end="\r", flush=True)
		temp_downloads_path = os.path.join(current_path, "temp downloads")
		processing.download_url_files(entries, temp_downloads_path)

		ascii_frames_path = os.path.join(current_path, "..", "ascii-frames")
		if not os.path.exists(ascii_frames_path):
			os.mkdir(ascii_frames_path)

		if not minimal_printing:
			print("\nProcessing", end="\r", flush=True)

		extra_variations_info = {}
		for entry in entries:
			url_name = entry["url_name"]
			extension = entry["extension"]
			url_file_path = os.path.join(temp_downloads_path, url_name + "." + extension)
			for variation in entry["variations"]:
				displayed_name_in_quotes = "'{}'".format(variation["displayed_name"])
				info = {
					"ascii_frames_path": ascii_frames_path,
					"url_file_path": url_file_path,
					"url_name": url_name,
					"extension": extension,
					"id": variation["id"],
					"displayed_name_in_quotes": displayed_name_in_quotes,
					"palette": variation["palette"],
					"width": variation["width"],
					"height": variation["height"],
					"minimal_printing": minimal_printing,
					"frame_skipping": frame_skipping,
					"new_width_stretched": new_width_stretched,
					"max_bytes_per_file": max_bytes_per_file,
					"frames_to_update_stats": frames_to_update_stats
				}
				# print("\nProcessing {}".format(displayed_name_in_quotes), end="\r", flush=True)
				extra_variations_info[variation["id"]] = processing.process_frames(info)

		processing.remove_url_files(temp_downloads_path)

		# print the time it took to run the program
		time_elapsed = time.time() - t0
		minutes = floor(time_elapsed / 60)
		seconds = floor(time_elapsed % 60)
		# TODO: The reason I don't just print the elapsed time, instead of passing it to Node.js,
		# is because when I print extra_variations_info and the elapsed time information after each other,
		# they get concatenated at Node.js' side for some reason.
		# time.sleep() or sys.stdout.write don't seem to fix this.
		print(str({
			"extra_variations_info": extra_variations_info,
			"elapsed": {
				"minutes": minutes,
				"seconds": seconds
			}
		}), end="\r", flush=True)
		# print("\nDone! {} minutes and {} seconds".format(minutes, seconds))
	except Exception as e:
		# Python child processes can't print to the terminal, so this will get Node.js to print any Python errors
		raise e

if __name__ == '__main__':
    main()