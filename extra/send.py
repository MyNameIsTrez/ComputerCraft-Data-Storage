import requests
import json

url = 'http://joppekoers.nl:1337'
myobj = {
	'password': 'trez',
	'data': [
		# NEWGROUNDS
		{
			'url': 'https://uploads.ungrounded.net/alternate/1448000/1448414_alternate_96550.720p.mp4',
			'name': 'ten years later',
			'extension': 'mp4'
		},
		{
			'url': 'https://uploads.ungrounded.net/alternate/1443000/1443835_alternate_95750.720p.mp4',
			'name': 'takeout',
			'extension': 'mp4'
		},
		{
			'url': 'http://uimg.ngfiles.com/icons/7349/7349981_large.png?f1578283262',
			'name': 'wavetro logo',
			'extension': 'png'
		},
	]
}

print(str(myobj))
a = str(myobj)

# headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
# x = requests.post(url, data = json.dumps(myobj), headers = headers)

# x = requests.post(url, data = myobj)
x = requests.post(url, data = a)