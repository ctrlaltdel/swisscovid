#!/usr/bin/env python3

import time
import sys
from datetime import datetime, timezone
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
    while True:
        packet = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", packet[:3])

        if plen == 40 and packet[16:18] == b'\x6f\xfd' and packet[20:22] == b'\x6f\xfd':
                mac = "{0[12]:02x}:{0[11]:02x}:{0[10]:02x}:{0[9]:02x}:{0[8]:02x}:{0[7]:02x}".format(packet)

                parsed_packet = {
                        'ts': datetime.now(timezone.utc).isoformat(),
                        'mac': mac,
                        'proximity': hexlify(packet[22:38]).decode('ascii'),
                        'aem': hexlify(packet[38:42]).decode('ascii')
                }

                return(parsed_packet)

if __name__ == '__main__':
    sock = open_bluetooth()

    try:
        while True:
            try:
                print(json.dumps(process_packet(sock)))
                sys.stdout.flush()

            except bluez.error as e:
                time.sleep(10)
                print("Bluetooth failed with error {}, reconnecting".format(e), file=sys.stderr)
                sock = open_bluetooth()

    except KeyboardInterrupt:
        pass
