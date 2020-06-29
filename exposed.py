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

START = arrow.get('2020-06-15T10:00:00+00:00')
BATCH_LENGTH = 2 * 60 * 60 * 1000

timestamp = int(START.format("X")) * 1000

while True:
	batch_release_time = timestamp - (timestamp % BATCH_LENGTH)
	r = requests.get(URL.format(batch_release_time))

	try:
		print(r.json())
	except JSONDecodeError:
		print('Error: ', timestamp, r.content)

	sys.stdout.flush()

	timestamp += BATCH_LENGTH

	if timestamp > int(arrow.now().format('X')) * 1000:
		sys.exit(0)
