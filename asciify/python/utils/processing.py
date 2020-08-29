import os
import time
from math import floor
import requests
import cv2
from PIL import Image

# Utils
import utils.char as char
import utils.outputting as outputting


def download_url_files(entries, temp_downloads_path, f):
	if not os.path.exists(temp_downloads_path):
		os.mkdir(temp_downloads_path)
	for entry in entries:
		filename = entry["url_name"]
		outputting.output(f, "'{}'".format(filename))
		r = requests.get(entry["url"], stream=True)
		file_path = os.path.join(temp_downloads_path, filename + "." + entry["extension"])
		with open(file_path, "wb") as url_file:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					url_file.write(chunk)


def remove_url_files(temp_downloads_path):
	for name in os.listdir(temp_downloads_path):
		if name != ".empty":
			os.remove(os.path.join(temp_downloads_path, name))


def process_frames(info):
	if info["minimal_printing"]:
		outputting.output(info["f"], "Processing {}".format(info["displayed_name_in_quotes"]))

	if info["extension"] == "mp4":
		info["video"] = cv2.VideoCapture(info["url_file_path"])
		info["old_image"] = None
	else:
		info["video"] = None
		info["old_image"] = Image.open(info["url_file_path"])

	info["new_width"] = get_new_width(info)

	# Create a folder for storing the ASCII frames for this variation.
	info["ascii_frames_variation_path"] = os.path.join(info["ascii_content_path"], info["id"])
	if not os.path.exists(info["ascii_frames_variation_path"]):
		os.mkdir(info["ascii_frames_variation_path"])

	info["frame_count"] = 0
	info["i"] = 0

	if info["extension"] == "mp4":
		info = process_mp4_frames(info)
	elif info["extension"] == "gif":
		info = process_gif_frames(info)
	elif info["extension"] == "jpeg" or info["extension"] == "png" or info["extension"] == "jpg":
		info = process_image_frame(info)
	else:
		outputting.output(info["f"], "Entered an invalid file extension; only files with mp4/gif/png/jpeg/jpg extensions are accepted!")
	
	if info["minimal_printing"]:
		outputting.output(info["f"], "Finished processing {}".format(info["displayed_name_in_quotes"]))

	return {
		"frame_files_count": info["frame_files_count"],
		"frame_count": info["frame_count"]
	}


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
			outputting.output(info["f"], "Can't load!")
	else:
		outputting.output(info["f"], "Entered an invalid file extension; only files with mp4/gif/png/jpeg/jpg extensions are accepted!")

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
		info["output_file"] = create_output_file(info["ascii_frames_variation_path"], info["frame_files_count"])
		info["frame_files_count"] += 1
	return info


def process_mp4_frames(info):
	actual_frame_count = int(info["video"].get(cv2.CAP_PROP_FRAME_COUNT))
	info["final_frame_count"] = floor(actual_frame_count / info["frame_skipping"])
	info["file_byte_count"] = 0
	info["output_file"] = create_output_file(info["ascii_frames_variation_path"], 1)
	info["frame_files_count"] = 2
	info["start_time"] = time.time()
	while True:
		info["start_frame_time"] = time.time()
		has_frames, cv2_frame = info["video"].read()
		if has_frames:
			if info["i"] % info["frame_skipping"] == 0:
				info["frame_count"] += 1
				info = try_create_new_output_file(info)
				# cv2_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
				cv2_frame = cv2.resize(cv2_frame, (info["new_width"] - 1, info["height"]))
				info["frame"] = Image.fromarray(cv2_frame)  # pil pixels can be read faster than cv2 pixels, according to my tests
				info["get_frame_time"] = time.time() - info["start_frame_time"]
				info = process_frame(info)
			info["i"] += 1
		else:
			info["video"].release()
			info["output_file"].close()
			info["frame_files_count"] -= 1
			return info


def process_gif_frames(info):
	info["final_frame_count"] = None
	info["file_byte_count"] = 0
	info["output_file"] = create_output_file(info["ascii_frames_variation_path"], 1)
	info["frame_files_count"] = 2
	info["start_time"] = time.time()
	try:
		while True:
			info["start_frame_time"] = time.time()
			if info["i"] % info["frame_skipping"] == 0:
				info["frame_count"] += 1
				info = try_create_new_output_file(info)
				info["frame"] = info["old_image"].resize((info["new_width"] - 1, info["height"]), Image.ANTIALIAS)
				info["get_frame_time"] = time.time() - info["start_frame_time"]
				info = process_frame(info)
				info["old_image"].seek(info["old_image"].tell() + 1)  # gets the next frame
			info["i"] += 1
	except:
		# this part gets reached when the code tries to find the next frame, while it has reached the end of the gif
		info["old_image"].close()
		info["output_file"].close()
		info["frame_files_count"] -= 1
		return info


def process_image_frame(info):
	info["frame_count"] += 1
	info["final_frame_count"] = 1
	info["file_byte_count"] = 0
	info["output_file"] = create_output_file(info["ascii_frames_variation_path"], 1)
	info["frame_files_count"] = 1
	info["start_time"] = time.time()
	info["start_frame_time"] = time.time()
	info["frame"] = info["old_image"].resize((info["new_width"] - 1, info["height"]), Image.ANTIALIAS)
	# frame = old_image.resize((new_width - 1, info["height"]), Image.NEAREST)
	# frame = old_image.resize((new_width - 1, info["height"]), Image.BILINEAR)
	# frame = old_image.resize((new_width - 1, info["height"]), Image.BICUBIC)
	# frame = frame.convert("RGB")
	info["old_image"].close()
	info["get_frame_time"] = time.time() - info["start_frame_time"]
	info = process_frame(info)
	info["output_file"].close()
	return info


def process_frame(info):
	prepare_loop_start_time = time.time()

	# not sure if it is necessary to convert the frame into RGBA!
	# load the pixels of the frame
	# frame_pixels = info["frame"].convert("RGBA").load()

	# initializes empty variables for the coming "for y, for x" loop
	prev_char = None
	prev_char_count = 0
	string = ""

	# the \n character at the end of every line needs to have one spot reserved
	# this should ideally be done at the resizing of the frame stage instead!
	modified_width = info["new_width"] - 1

	prepare_loop_end_time = time.time()

	# measure the time it takes for the coming "for y, for x" loop to execute
	pixel_loop_start_time = time.time()
	
	newimage = info["frame"].quantize(palette=info["palette_img"], dither=True)
	palette = newimage.getpalette() # TODO: I don't think this getpalette() call is necessary!
	palette = info["palette"]
	for y in range(info["height"]):
		for x in range(modified_width):
			string += char.get_char(palette, newimage.getpixel((x, y)))
		# the last character in a frame doesn't need a return character after it
		if y < info["height"] - 1:
			# add a return character to the end of each horizontal line,
			# so ComputerCraft can draw the entire frame with one write() statement
			string += "\\n"

	pixel_loop_end_time = time.time()

	write_start_time = time.time()

	# gives each frame its own line in the outputted file, so lines can easily be found and parsed
	if info["frame_count"] > 1:
		final_string = "\n" + string
	else:
		final_string = string

	info["output_file"].write(final_string)

	write_end_time = time.time()

	info["prepare_loop_time"] = prepare_loop_end_time - prepare_loop_start_time
	info["pixel_loop_time"] = pixel_loop_end_time - pixel_loop_start_time
	info["write_time"] = write_end_time - write_start_time

	if info["frame_count"] % info["frames_to_update_stats"] == 0 or info["frame_count"] == info["final_frame_count"]:
		print_stats(info)

	info["file_byte_count"] += len(final_string.encode("utf8")) # TODO: utf8 encoding necessary?

	return info


def print_stats(info):
	# progress
	progress = "frame " + str(info["frame_count"]) + "/"
	if info["final_frame_count"]:
		progress = progress + str(info["final_frame_count"])
	else:
		progress = progress + "?"

	elapsed = time.time() - info["start_frame_time"]

	# eta
	if info["final_frame_count"]:
		frames_left = info["final_frame_count"] - info["frame_count"]
		seconds_left = elapsed * frames_left

		eta_hours   = floor(seconds_left / 3600)
		eta_minutes = floor(seconds_left / 60) % 60
		eta_seconds = floor(seconds_left) % 60

		# makes sure each value is always 2 characters wide when printed
		eta_hours =   ("0" if eta_hours   < 10 else "") + str(eta_hours)
		eta_minutes = ("0" if eta_minutes < 10 else "") + str(eta_minutes)
		eta_seconds = ("0" if eta_seconds < 10 else "") + str(eta_seconds)

		eta = "{}:{}:{} left".format(eta_hours, eta_minutes, eta_seconds)
	else:
		eta = "??:??:?? left"

	# time_passed_str
	if elapsed > 0:
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
		
		time_passed_str = "{}:{}:{} passed".format(spent_hours, spent_minutes, spent_seconds)
	else:
		time_passed_str = "??:??:?? passed"

	speed_frames_processed = "speed: {} frames/s".format(       floor(1 / elapsed)                   if elapsed > 0                   else "1000+")
	speed_get_frame        = "get frame: {} frames/s".format(   floor(1 / info["get_frame_time"])    if info["get_frame_time"] > 0    else "1000+")
	speed_prepare_loop     = "prepare loop: {} frames/s".format(floor(1 / info["prepare_loop_time"]) if info["prepare_loop_time"] > 0 else "1000+")
	speed_pixel_loop       = "pixel loop: {} frames/s".format(  floor(1 / info["pixel_loop_time"])   if info["pixel_loop_time"] > 0   else "1000+")
	speed_write            = "write: {} frames/s".format(       floor(1 / info["write_time"])        if info["write_time"] > 0        else "1000+")

	# outputting.output(info["f"], " | ".join((info["displayed_name_in_quotes"], progress, eta, time_passed_str, speed_frames_processed)))
	if not info["minimal_printing"]:
		outputting.output(info["f"], " | ".join((info["displayed_name_in_quotes"], progress, eta, time_passed_str, speed_frames_processed, speed_get_frame, speed_prepare_loop, speed_pixel_loop, speed_write)))
