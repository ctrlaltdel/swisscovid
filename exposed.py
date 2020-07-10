#!/usr/bin/env python3

import sys
import time
import requests
import arrow
import exposed_pb2
from simplejson.errors import JSONDecodeError

#URL = 'https://www.pt-d.bfs.admin.ch/v1/exposed/{}'
#URL = 'https://www.pt-t.bfs.admin.ch/v1/exposed/{}'
#URL = 'https://www.pt-a.bfs.admin.ch/v1/exposed/{}'
URL = 'https://www.pt.bfs.admin.ch/v1/exposed/{}'

BATCH_LENGTH = 2 * 60 * 60 * 1000

timestamp = int(arrow.now().format('X')) * 1000

exposed = []

while True:
	batch_release_time = timestamp - (timestamp % BATCH_LENGTH)
	r = requests.get(URL.format(batch_release_time))

	exposed_list = exposed_pb2.ProtoExposedList.FromString(r.content)


	if exposed_list.batchReleaseTime:
		exposed = exposed + list(exposed_list.exposed)
		print(exposed_list)
		sys.stdout.flush()
	else:
		break

	timestamp -= BATCH_LENGTH

print({'batchReleaseTime': 'ALL', 'exposed': exposed})
