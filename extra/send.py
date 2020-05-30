import requests
import json


# NEWGROUNDS
# {
# 	'url': 'https://uploads.ungrounded.net/alternate/1448000/1448414_alternate_96550.720p.mp4',
# 	'name': 'ten years later',
# 	'extension': 'mp4'
# },
# {
# 	'url': 'https://uploads.ungrounded.net/alternate/1443000/1443835_alternate_95750.720p.mp4',
# 	'name': 'takeout',
# 	'extension': 'mp4'
# },
# {
# 	'url': 'http://uimg.ngfiles.com/icons/7349/7349981_large.png?f1578283262',
# 	'name': 'wavetro logo',
# 	'extension': 'png'
# },


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

url = 'http://joppekoers.nl:1337'
myobj = {
	'password': 'MyNameIsTrez',
	'data': [
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
				{
					"char_type": "grayscale",
					"width": 426,
					"height": 160
				},
				# {
				# 	"char_type": "color",
				# 	"width": 426,
				# 	"height": 160
				# }
			]
		},
	]
}

print(str(myobj))
# a = str(myobj)

# headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
# x = requests.post(url, data = json.dumps(myobj), headers = headers)

# x = requests.post(url, data = myobj)
x = requests.post(url, data = myobj)