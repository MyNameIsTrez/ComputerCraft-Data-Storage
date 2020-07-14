import os
import time
from math import floor
import requests
import cv2
from PIL import Image

# Utils
import utils.char as char


def download_url_files(files_info, temp_downloads_path):
	if not os.path.exists(temp_downloads_path):
		os.mkdir(temp_downloads_path)
	for file_info in files_info:
		filename = file_info["url_name"]
		print("    '" + filename + "'")
		r = requests.get(file_info["url"], stream=True)
		file_path = os.path.join(temp_downloads_path, filename + "." + file_info["extension"])
		with open(file_path, "wb") as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
			f.close()  # Necessary?


def remove_url_files(temp_downloads_path):
	for name in os.listdir(temp_downloads_path):
		if name != ".empty":
			os.remove(os.path.join(temp_downloads_path, name))


def process_frames(info):
	if info["extension"] == "mp4":
		info["video"] = cv2.VideoCapture(info["url_file_path"])
		info["old_image"] = None
	else:
		info["video"] = None
		info["old_image"] = Image.open(info["url_file_path"])

	info["new_width"] = get_new_width(info)

	# Create a folder for storing the ASCII frames for this variation.
	info["ascii_frames_variation_path"] = os.path.join(info["ascii_frames_path"], info["id"])
	if not os.path.exists(info["ascii_frames_variation_path"]):
		os.mkdir(info["ascii_frames_variation_path"])

	if info["extension"] == "mp4":
		info = process_mp4_frames(info)
	elif info["extension"] == "gif":
		info = process_gif_frames(info)
	elif info["extension"] == "jpeg" or info["extension"] == "png" or info["extension"] == "jpg":
		info = process_image_frame(info)
	else:
		print("Entered an invalid file extension! Only mp4, gif, jpeg, png and jpg extensions are allowed.")

	# output_info_file = create_output_file(output_folder_name, "info")
	# string = "{frame_count=" + str(info["used_frame_count"]) + ",width=" + str(info["new_width"]) + ",height=" + str(info["height"]) + ",data_files=" + str(info["data_frames_count"]) + "}"
	# output_info_file.write(string)
	# output_info_file.close()
	print()


def get_new_width(info):
	if info["extension"] == "mp4":
		# get information about the video file
		old_width = info["video"].get(cv2.CAP_PROP_FRAME_WIDTH)
		old_height = info["video"].get(cv2.CAP_PROP_FRAME_HEIGHT)
	elif info["extension"] == "gif" or info["extension"] == "jpeg" or info["extension"] == "png" or info["extension"] == "jpg":
		try:
			# TODO: refactor this into a one-liner
			old_width = info["old_image"].size[0]
			old_height = info["old_image"].size[1]
		except IOError:
			print("Can't load!")
	else:
		print("Entered an invalid file type; only mp4, gif, jpeg, png and jpg extensions are allowed!")

	if info["new_width_stretched"]:
		return info["width"]
	else:
		return int(info["height"] * old_width / old_height)


def create_output_file(folder, name):
	output_path = os.path.join(folder, str(name) + ".txt")
	return open(output_path, "w")


def try_create_new_output_file(info):
	if info["file_byte_count"] >= info["max_bytes_per_file"]:
		info["file_byte_count"] = 0
		if info["output_file"]:
			info["output_file"].close()
		info["output_file"] = create_output_file(info["ascii_frames_variation_path"], info["data_frames_count"])
		info["data_frames_count"] += 1
	return info


def process_mp4_frames(info):
	i = 0
	info["used_frame_count"] = 0
	actual_frame_count = int(info["video"].get(cv2.CAP_PROP_FRAME_COUNT))
	info["new_frame_count"] = floor(actual_frame_count / info["frame_skipping"])
	info["file_byte_count"] = 0
	info["output_file"] = create_output_file(info["ascii_frames_variation_path"], 1)
	info["data_frames_count"] = 2
	info["start_time"] = time.time()
	while True:
		info["start_frame_time"] = time.time()
		has_frames, cv2_frame = info["video"].read()
		if has_frames:
			if i % info["frame_skipping"] == 0:
				info["used_frame_count"] += 1
				info = try_create_new_output_file(info)
				# cv2_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
				cv2_frame = cv2.resize(cv2_frame, (info["new_width"] - 1, info["height"]))
				info["frame"] = Image.fromarray(cv2_frame)  # pil pixels can be read faster than cv2 pixels, according to my tests
				info["get_frame_time"] = time.time() - info["start_frame_time"]
				info = process_frame(info)
			i += 1
		else:
			info["video"].release()
			info["output_file"].close()
			info["data_frames_count"] -= 1
			return info


def process_gif_frames(info):
	i = 0
	info["used_frame_count"] = 0
	info["new_frame_count"] = None
	info["file_byte_count"] = 0
	info["output_file"] = create_output_file(info["ascii_frames_variation_path"], 1)
	info["data_frames_count"] = 2
	info["start_time"] = time.time()
	try:
		while True:
			info["start_frame_time"] = time.time()
			if i % info["frame_skipping"] == 0:
				info["used_frame_count"] += 1
				info = try_create_new_output_file(info)
				info["frame"] = info["old_image"].resize((info["new_width"] - 1, info["height"]), Image.ANTIALIAS)
				info["get_frame_time"] = time.time() - info["start_frame_time"]
				info = process_frame(info)
				info["old_image"].seek(info["old_image"].tell() + 1)  # gets the next frame
			i += 1
	except:
		# this part gets reached when the code tries to find the next frame, while it has reached the end of the gif
		info["output_file"].close()
		info["data_frames_count"] -= 1
		return info


def process_image_frame(info):
	info["used_frame_count"] = 1
	info["new_frame_count"] = 1
	info["file_byte_count"] = 0
	info["output_file"] = create_output_file(info["ascii_frames_variation_path"], 1)
	info["data_frames_count"] = 1
	info["start_time"] = time.time()
	info["start_frame_time"] = time.time()
	info["frame"] = info["old_image"].resize((info["new_width"] - 1, info["height"]), Image.ANTIALIAS)
	# frame = old_image.resize((new_width - 1, info["height"]), Image.NEAREST)
	# frame = old_image.resize((new_width - 1, info["height"]), Image.BILINEAR)
	# frame = old_image.resize((new_width - 1, info["height"]), Image.BICUBIC)
	# frame = frame.convert("RGB")
	info["get_frame_time"] = time.time() - info["start_frame_time"]
	info = process_frame(info)
	info["output_file"].close()
	return info


def process_frame(info):
	preparing_loop_start_time = time.time()

	# not sure if it is necessary to convert the frame into RGBA!
	# load the pixels of the frame
	frame_pixels = info["frame"].convert("RGBA").load()

	# initializes empty variables for the coming "for y, for x" loop
	prev_char = None
	prev_char_count = 0
	string = ""

	# the \n character at the end of every line needs to have one spot reserved
	# this should ideally be done at the resizing of the frame stage instead!
	modified_width = info["new_width"] - 1

	preparing_loop_end_time = time.time()

	# measure the time it takes for the coming "for y, for x" loop to execute
	looping_start_time = time.time()

	for y in range(info["height"]):
		for x in range(modified_width):
			# TODO: Let NP access the frame_pixels array directly, instead of looping through each pixel manually!
			string += char.get_char(frame_pixels[x, y], info["palette"])

		# the last character in a frame doesn't need a return character after it
		if y < info["height"] - 1:
			# add a return character to the end of each horizontal line,
			# so ComputerCraft can draw the entire frame with one write() statement
			string += "\\n"

	looping_end_time = time.time()

	writing_start_time = time.time()

	# gives each frame its own line in the outputted file, so lines can easily be found and parsed
	if info["used_frame_count"] > 1:
		final_string = string
	else:
		final_string = "\n" + string

	info["output_file"].write(final_string)

	writing_end_time = time.time()

	info["preparing_loop_time"] = preparing_loop_end_time - preparing_loop_start_time
	info["looping_time"] = looping_end_time - looping_start_time
	info["writing_time"] = writing_end_time - writing_start_time

	if info["used_frame_count"] % info["frames_to_update_stats"] == 0 or info["used_frame_count"] == info["new_frame_count"]:
		print_stats(info)

	info["file_byte_count"] += len(final_string.encode("utf8")) # TODO: utf8 encoding necessary?

	return info


def print_stats(info):
	file_name_str = "'" + info["displayed_name"] + "', "

	# progress
	progress = "frame " + str(info["used_frame_count"]) + "/"
	if info["new_frame_count"]:
		progress = progress + str(info["new_frame_count"])
	else:
		progress = progress + "?"

	# speed of processing the frame
	elapsed = time.time() - info["start_frame_time"]
	if elapsed > 0:
		processed_fps = floor(1 / elapsed)

		time_spent = time.time() - info["start_time"]

		spent_hours = floor(time_spent / 3600)
		spent_minutes = floor(time_spent / 60) % 60
		spent_seconds = floor(time_spent) % 60

		# makes sure each value is always 2 characters wide when printed
		if spent_hours < 10:
			spent_hours = "0" + str(spent_hours)
		if spent_minutes < 10:
			spent_minutes = "0" + str(spent_minutes)
		if spent_seconds < 10:
			spent_seconds = "0" + str(spent_seconds)
		
		time_spent_str = ", {}:{}:{} passed".format(spent_hours, spent_minutes, spent_seconds)
	else:
		processed_fps = "1000+"
		time_spent_str = ", ??:??:?? passed"
	speed = ", speed: {} frames/s".format(processed_fps)

	# speed of getting the frame
	if info["get_frame_time"] > 0:
		processed_fps = floor(1 / info["get_frame_time"])
	else:
		processed_fps = "1000+"
	speed_2 = ", get frame: {} frames/s".format(processed_fps)

	# preparing for the "for y, for x" loop
	if info["preparing_loop_time"] > 0:
		processed_fps = floor(1 / info["preparing_loop_time"])
	else:
		processed_fps = "1000+"
	speed_3 = ", preparing loop: {} frames/s".format(processed_fps)

	# speed of the "for y, for x" loop
	if info["looping_time"] > 0:
		processed_fps = floor(1 / info["looping_time"])
	else:
		processed_fps = "1000+"
	speed_4 = ", pixel loop: {} frames/s".format(processed_fps)

	# writing speed
	if info["writing_time"] > 0:
		processed_fps = floor(1 / info["writing_time"])
	else:
		processed_fps = "1000+"
	speed_5 = ", writing: {} frames/s".format(processed_fps)

	# calculate how long it should take for the program to finish
	if info["new_frame_count"]:
		frames_left = info["new_frame_count"] - info["used_frame_count"]
		seconds_left = elapsed * frames_left

		eta_hours = floor(seconds_left / 3600)
		eta_minutes = floor(seconds_left / 60) % 60
		eta_seconds = floor(seconds_left) % 60

		# makes sure each value is always 2 characters wide when printed
		if eta_hours < 10:
			eta_hours = "0" + str(eta_hours)
		if eta_minutes < 10:
			eta_minutes = "0" + str(eta_minutes)
		if eta_seconds < 10:
			eta_seconds = "0" + str(eta_seconds)

		eta = ", {}:{}:{} left".format(eta_hours, eta_minutes, eta_seconds)
	else:
		eta = ", ??:??:?? left"

	# clears the line that will be printed on of any straggling characters
	tab = "    "

	print(tab + file_name_str + progress + speed + eta + time_spent_str + tab, end="\r", flush=True)

	# sys.stdout.write("\033[F") # Cursor up one line
	# sys.stdout.write("\033[K") # Clear to the end of line

	# print(tab + progress + speed + eta, end="\r", flush=True)
	# print(tab + progress + speed + speed_2 + speed_3 + speed_4 + speed_5 + eta, end="\r", flush=True)