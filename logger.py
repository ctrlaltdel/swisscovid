#!/usr/bin/env python3

import time
import sys
import datetime
import struct
import json
import bluetooth._bluetooth as bluez
from binascii import hexlify

DEVICE = 0
OGF_LE_CTL = 0x08
OCF_LE_SET_SCAN_ENABLE = 0x000C

def open_bluetooth():
    sock = bluez.hci_open_dev(DEVICE)

    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, b'\x01\x00')

    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    return(sock)

def process_packet(sock):
    packet = sock.recv(255)
    ptype, event, plen = struct.unpack("BBB", packet[:3])

    if plen == 40 and packet[16:18] == b'\x6f\xfd' and packet[20:22] == b'\x6f\xfd':
        parsed_packet = {
            'ts': datetime.datetime.now().isoformat(),
            'mac': "{0[12]:x}:{0[11]:x}:{0[10]:x}:{0[9]:x}:{0[8]:x}:{0[7]:x}".format(packet),
            'proximity': hexlify(packet[22:38]).decode('ascii'),
            'aem': hexlify(packet[38:42]).decode('ascii')
        }

        #print(ptype, event, plen)
        #print(hexlify(packet))
        print(json.dumps(parsed_packet))
        sys.stdout.flush()

sock = open_bluetooth()

try:
    while True:
        try:
            process_packet(sock)
        except bluez.error:
            time.sleep(30)
            sock = open_bluetooth()

except KeyboardInterrupt:
    pass
