from utils import char_blue as char
from PIL import Image

info = {}

info["old_image"] = Image.open("rick_astley.png")

info["palette"] = "color"

scale = 1
info["height"] = int(160 * scale)
info["new_width"] = int(426 * scale)

info["frame"] = info["old_image"].resize((info["new_width"] - 1, info["height"]), Image.ANTIALIAS)

char.dither_frame(info)

info["dithered_frame"].show()