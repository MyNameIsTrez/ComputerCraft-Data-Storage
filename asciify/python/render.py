import os, sys, time, json
from math import floor

# From the utils folder
from utils import processing
from utils import outputting
from utils import char


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
	with open('conversion-progress.txt', 'w') as f:
		try:
			entries = read_in()

			t0 = time.time()

			outputting.output(f, "Downloading URL files")
			temp_downloads_path = os.path.join(current_path, "temp-downloads")
			processing.download_url_files(entries, temp_downloads_path, f)

			ascii_content_path = os.path.join(current_path, "..", "ascii-content")
			if not os.path.exists(ascii_content_path):
				os.mkdir(ascii_content_path)

			if not minimal_printing:
				outputting.output(f, "Processing")

			extra_variations_info = {}
			for entry in entries:
				url_name = entry["url_name"]
				extension = entry["extension"]
				url_file_path = os.path.join(temp_downloads_path, url_name + "." + extension)
				for variation in entry["variations"]:
					displayed_name_in_quotes = "'{}'".format(variation["displayed_name"])
					info = {
						"f": f,
						"ascii_content_path": ascii_content_path,
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
						"frames_to_update_stats": frames_to_update_stats,
						"palette_img": char.get_palette_img(variation["palette"])
					}
					extra_variations_info[variation["id"]] = processing.process_frames(info)

			# gets caught by Node.js, doesn't get written to the terminal
			print(json.dumps(extra_variations_info))

			processing.remove_url_files(temp_downloads_path)

			# print the time it took to run the program
			time_elapsed = time.time() - t0
			minutes = floor(time_elapsed / 60)
			seconds = floor(time_elapsed % 60)
			outputting.output(f, "Done! {} minutes and {} seconds".format(minutes, seconds))
		except Exception as e:
			raise e

if __name__ == '__main__':
    main()
