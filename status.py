#!/usr/bin/env python3

import json
import bluetooth._bluetooth as bluez
from pprint import pprint
from logger import open_bluetooth, process_packet

def save(data):
    with open('seen.json', 'w') as outfile:
        json.dump(data, outfile)

def load():
    with open('seen.json', 'r') as infile:
        return(json.load(infile))

def display(seen):
    for mac in seen.keys():
        print("{}: {} {}".format(mac, seen[mac]['first_ts'], seen[mac]['last_ts']))
    print()

seen = load()

sock = open_bluetooth()

try:
    while True:
        try:
            packet = process_packet(sock)
            # print(packet)
            mac = packet['mac']
            ts = packet['ts']

            if not mac in seen:
                seen[mac] = {}
                seen[mac]['first_ts'] = ts
            else:
                seen[mac]['last_ts'] = ts

        except bluez.error as e:
            time.sleep(10)
            print("Bluetooth failed with error {}, reconnecting".format(e), file=sys.stderr)
            sock = open_bluetooth()
        
        display(seen)

except KeyboardInterrupt:
    save(seen)
    pass
