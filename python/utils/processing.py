import os
import time
from math import floor
import requests
import cv2
from PIL import Image

# Utils
import utils.dithering as dithering

# Function I stole from StackOverflow:
# https://stackoverflow.com/a/35844551
def download_files(files_info, currentPath):
	for file_info in files_info['data']:
		r = requests.get(file_info['url'], stream=True)
		fileName = os.path.join(currentPath, 'temp downloads/', file_info['name'] + '.' + file_info['extension'])
		with open(fileName, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
			f.close() # Necessary?


def process_frames(full_file_name, max_width, max_height, frame_skipping, extended_chars, currentPath, new_width_stretched, max_bytes_per_file, frames_to_update_stats):
	extension = full_file_name.split('.')[1]  # get the extension after the '.'
	# get the name before the '.', and optionally add '_extended'
	file_name = full_file_name.split('.')[0] + (' extended' if extended_chars else '')
	input_path = os.path.join(currentPath, 'temp downloads/' , full_file_name)

	output_file_name = file_name.replace(' ', '_')

	print('Processing \'' + file_name + '\'')

	if extension == 'mp4':
		video = cv2.VideoCapture(input_path)
		old_image = None
	else:
		video = None
		old_image = Image.open(input_path)

	new_height = max_height
	new_width = get_new_width(extension, video, old_image, input_path, new_height, max_width, new_width_stretched)

	animationsPath = os.path.join(currentPath, 'animations/')
	if not os.path.exists(animationsPath):
		os.mkdir(animationsPath)

	output_folder_size_name = os.path.join(animationsPath, 'size_' + str(new_width) + 'x' + str(new_height))
	if not os.path.exists(output_folder_size_name):
		os.mkdir(output_folder_size_name)

	output_folder_name = os.path.join(output_folder_size_name, output_file_name)
	if not os.path.exists(output_folder_name):
		os.mkdir(output_folder_name)

	output_data_folder_name = os.path.join(output_folder_name , 'data/')
	if not os.path.exists(output_data_folder_name):
		os.mkdir(output_data_folder_name)

	if extension == 'mp4':
		used_frame_count, data_frames_count = process_mp4_frames(output_data_folder_name, video, frame_skipping, new_width, new_height, extended_chars, max_bytes_per_file, frames_to_update_stats)
	elif extension == 'gif':
		used_frame_count, data_frames_count = process_gif_frames(output_data_folder_name, old_image, new_width, new_height, frame_skipping, extended_chars, max_bytes_per_file, frames_to_update_stats)
	elif extension == 'jpeg' or extension == 'png' or extension == 'jpg':
		used_frame_count, data_frames_count = process_image_frame(output_data_folder_name, old_image, new_width, new_height, extended_chars, frames_to_update_stats)
	else:
		print('Entered an invalid file type; only mp4, gif, jpeg, png and jpg extensions are allowed!')

	output_info_file = create_output_file(output_folder_name, 'info')
	string = '{frame_count=' + str(used_frame_count) + ',width=' + str(new_width) + ',height=' + str(new_height) + ',data_files=' + str(data_frames_count) + '}'
	output_info_file.write(string)
	output_info_file.close()


def get_new_width(extension, video, old_image, input_path, new_height, max_width, new_width_stretched):
	if extension == 'mp4':
		# get information about the video file
		old_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
		old_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
	elif extension == 'gif' or extension == 'jpeg' or extension == 'png' or extension == 'jpg':
		try:
			old_width = old_image.size[0]
			old_height = old_image.size[1]
		except IOError:
			print('Can\'t load!')
	else:
		print('Entered an invalid file type; only mp4, gif, jpeg, png and jpg extensions are allowed!')

	if new_width_stretched:
		return max_width
	else:
		return int(new_height * old_width / old_height)


def create_output_file(folder, name):
	output_path = folder + '/' + str(name) + '.txt'
	return open(output_path, 'w')


def try_create_new_output_file(line_num, file_byte_count, output_file, output_data_folder_name, data_frames_count, max_bytes_per_file):
	line_num += 1

	if file_byte_count >= max_bytes_per_file:
		file_byte_count = 0

		if output_file:
			output_file.close()

		output_file = create_output_file(output_data_folder_name, data_frames_count)

		data_frames_count += 1

		line_num = 1

	return line_num, file_byte_count, output_file, data_frames_count


def process_mp4_frames(output_data_folder_name, video, frame_skipping, new_width, new_height, extended_chars, max_bytes_per_file, frames_to_update_stats):
	i = 0
	used_frame_count = 0

	actual_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	new_frame_count = floor(actual_frame_count / frame_skipping)

	file_byte_count = 0
	output_file = create_output_file(output_data_folder_name, 1)
	data_frames_count = 2
	line_num = 0

	while True:
		start_frame_time = time.time()

		hasFrames, cv2_frame = video.read()

		if hasFrames:
			if i % frame_skipping == 0:
				used_frame_count += 1

				line_num, file_byte_count, output_file, data_frames_count = try_create_new_output_file(line_num, file_byte_count, output_file, output_data_folder_name, data_frames_count, max_bytes_per_file)

				# cv2_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)

				cv2_frame = cv2.resize(cv2_frame, (new_width - 1, new_height))

				pil_frame = Image.fromarray(cv2_frame)  # pil pixels can be read faster than cv2 pixels, it seems

				get_frame_time = time.time() - start_frame_time  # 40 frames/s

				file_byte_count += process_frame(pil_frame, used_frame_count, line_num, new_width, new_height, output_file, new_frame_count, start_frame_time, get_frame_time, extended_chars, frames_to_update_stats)
			i += 1
		else:
			video.release()
			output_file.close()

			return used_frame_count, data_frames_count - 1


def process_gif_frames(output_data_folder_name, old_image, new_width, new_height, frame_skipping, extended_chars, max_bytes_per_file, frames_to_update_stats):
	i = 0
	used_frame_count = 0

	file_byte_count = 0
	output_file = create_output_file(output_data_folder_name, 1)
	data_frames_count = 2
	line_num = 0

	try:
		while True:
			start_frame_time = time.time()

			if i % frame_skipping == 0:
				used_frame_count += 1

				line_num, file_byte_count, output_file, data_frames_count = try_create_new_output_file(line_num, file_byte_count, output_file, output_data_folder_name, data_frames_count, max_bytes_per_file)

				new_image = old_image.resize((new_width - 1, new_height), Image.ANTIALIAS)

				get_frame_time = time.time() - start_frame_time

				file_byte_count += process_frame(new_image, used_frame_count, line_num, new_width, new_height, output_file, None, start_frame_time, get_frame_time, extended_chars, frames_to_update_stats)

				old_image.seek(old_image.tell() + 1)  # gets the next frame
			i += 1
	except:
		# this part gets reached when the code tries to find the next frame, while it doesn't exist
		output_file.close()

		return used_frame_count, data_frames_count - 1


def process_image_frame(output_data_folder_name, old_image, new_width, new_height, extended_chars, frames_to_update_stats):
	data_frames_count = 1
	line_num = 0

	output_file = create_output_file(output_data_folder_name, 1)

	start_frame_time = time.time()

	new_image = old_image.resize((new_width - 1, new_height), Image.ANTIALIAS)
	# new_image = old_image.resize((new_width - 1, new_height), Image.NEAREST)
	# new_image = old_image.resize((new_width - 1, new_height), Image.BILINEAR)
	# new_image = old_image.resize((new_width - 1, new_height), Image.BICUBIC)

	# new_image = new_image.convert('RGB')

	used_frame_count = 1

	get_frame_time = time.time() - start_frame_time

	process_frame(new_image, used_frame_count, line_num, new_width, new_height, output_file, 1, start_frame_time, get_frame_time, extended_chars, frames_to_update_stats)

	output_file.close()

	return used_frame_count, data_frames_count


def process_frame(frame, used_frame_count, line_num, new_width, new_height, output_file, frame_count, start_frame_time, get_frame_time, extended_chars, frames_to_update_stats):
	preparing_loop_start_time = time.time()

	# not sure if it is necessary to convert the frame into RGBA!
	frame = frame.convert('RGBA')
	# load the pixels of the frame
	frame_pixels = frame.load()

	# initializes empty variables for the coming 'for y, for x' loop
	prev_char = None
	prev_char_count = 0
	string = ''

	# the \n character at the end of every line needs to have one spot reserved
	# this should ideally be done at the resizing of the frame stage instead!
	modified_width = new_width - 1

	preparing_loop_end_time = time.time()

	# measure the time it takes for the coming 'for y, for x' loop to execute
	looping_start_time = time.time()

	for y in range(new_height):
		for x in range(modified_width):
			pixel = frame_pixels[x, y]
			string += dithering.get_char(pixel, extended_chars)

		# the last character in a frame doesn't need a return character after it
		if y < new_height - 1:
			# add a return character to the end of each horizontal line,
			# so ComputerCraft can draw the entire frame with one write() statement
			string += '\\n'

	looping_end_time = time.time()

	writing_start_time = time.time()

	# gives each frame its own line in the outputted file, so lines can easily be found and parsed
	if line_num > 1:
		final_string = '\n' + string
	else:
		final_string = string

	output_file.write(final_string)

	writing_end_time = time.time()

	preparing_loop_time = preparing_loop_end_time - preparing_loop_start_time
	looping_time = looping_end_time - looping_start_time
	writing_time = writing_end_time - writing_start_time

	if used_frame_count % frames_to_update_stats == 0 or used_frame_count == frame_count:
		print_stats(used_frame_count, frame_count, start_frame_time, get_frame_time, preparing_loop_time, looping_time, writing_time)

		if used_frame_count == frame_count:
			print()

	string_byte_count = len(final_string.encode('utf8'))

	return string_byte_count


def print_stats(used_frame_count, frame_count, start_frame_time, get_frame_time, preparing_loop_time, looping_time, writing_time):
	# progress
	progress = 'Frame ' + str(used_frame_count) + '/'
	if frame_count:
		progress = progress + str(frame_count)
	else:
		progress = progress + '?'

	# speed of processing the frame
	elapsed = time.time() - start_frame_time
	if elapsed > 0:
		processed_fps = floor(1 / elapsed)
	else:
		processed_fps = '1000+'
	speed = ', speed: {} frames/s'.format(processed_fps)

	# speed of getting the frame
	if get_frame_time > 0:
		processed_fps = floor(1 / get_frame_time)
	else:
		processed_fps = '1000+'
	speed_2 = ', get frame: {} frames/s'.format(processed_fps)

	# preparing for the 'for y, for x' loop
	if preparing_loop_time > 0:
		processed_fps = floor(1 / preparing_loop_time)
	else:
		processed_fps = '1000+'
	speed_3 = ', preparing loop: {} frames/s'.format(processed_fps)

	# speed of the 'for y, for x' loop
	if looping_time > 0:
		processed_fps = floor(1 / looping_time)
	else:
		processed_fps = '1000+'
	speed_4 = ', pixel loop: {} frames/s'.format(processed_fps)

	# writing speed
	if writing_time > 0:
		processed_fps = floor(1 / writing_time)
	else:
		processed_fps = '1000+'
	speed_5 = ', writing: {} frames/s'.format(processed_fps)

	# calculate how long it should take for the program to finish
	if frame_count:
		frames_left = frame_count - used_frame_count
		seconds_left = elapsed * frames_left

		eta_hours = floor(seconds_left / 3600)
		eta_minutes = floor(seconds_left / 60) % 60
		eta_seconds = floor(seconds_left) % 60

		# makes sure each value is always 2 characters wide when printed
		if eta_hours < 10:
			eta_hours = '0' + str(eta_hours)
		if eta_minutes < 10:
			eta_minutes = '0' + str(eta_minutes)
		if eta_seconds < 10:
			eta_seconds = '0' + str(eta_seconds)

		eta = ', {}:{}:{} left'.format(eta_hours, eta_minutes, eta_seconds)
	else:
		eta = ', ? left'

	# clears the line that will be printed on of any straggling characters
	tab = '    '

	print(tab + progress + speed + eta, end='\r', flush=True)

	# sys.stdout.write("\033[F") # Cursor up one line
	# sys.stdout.write("\033[K") # Clear to the end of line

	# print(tab + progress + speed + eta, end='\r', flush=True)
	# print(tab + progress + speed + speed_2 + speed_3 + speed_4 + speed_5 + eta, end='\r', flush=True)