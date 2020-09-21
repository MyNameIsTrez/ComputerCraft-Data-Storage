from utils import char
from PIL import Image

info = {}

info["old_image"] = Image.open("rick_astley.png")

info["palette"] = "color"
info["height"] = 160
info["new_width"] = 426

info["frame"] = info["old_image"].resize((info["new_width"] - 1, info["height"]), Image.ANTIALIAS)

char.dither_frame(info)

info["dithered_frame"].show()