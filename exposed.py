#!/usr/bin/env python3

import sys
import time
import requests
import arrow
from simplejson.errors import JSONDecodeError

#URL = 'https://www.pt-d.bfs.admin.ch/v1/exposedjson/{}'
#URL = 'https://www.pt-t.bfs.admin.ch/v1/exposedjson/{}'
#URL = 'https://www.pt-a.bfs.admin.ch/v1/exposedjson/{}'
URL = 'https://www.pt.bfs.admin.ch/v1/exposedjson/{}'

BATCH_LENGTH = 2 * 60 * 60 * 1000

timestamp = int(arrow.now().format('X')) * 1000

exposed = []

while True:
	batch_release_time = timestamp - (timestamp % BATCH_LENGTH)
	r = requests.get(URL.format(batch_release_time))

	try:
		print(r.json())
		exposed = exposed + r.json()['exposed']
	except JSONDecodeError:
		if r.content == b'':
			break
		else:
			print('Error: ', timestamp, r.content)

	sys.stdout.flush()

	timestamp -= BATCH_LENGTH

print({'batchReleaseTime': 'ALL', 'exposed': exposed})
