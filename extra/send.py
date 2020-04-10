import requests

url = 'http://joppekoers.nl:1337'
myobj = {
	'password': 'trez',
	'data': [
	 	# NEWGROUNDS
		[
			'https://uploads.ungrounded.net/alternate/1448000/1448414_alternate_96550.720p.mp4',
			'ten years later',
			'mp4'
		],
		[
			'https://uploads.ungrounded.net/alternate/1443000/1443835_alternate_95750.720p.mp4',
			'takeout',
			'mp4'
		],
		[
			'http://uimg.ngfiles.com/icons/7349/7349981_large.png?f1578283262',
			'wavetro logo',
			'png'
		],
	]
}

x = requests.post(url, data = myobj)