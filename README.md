# SwissCovid learning tools

Tools for learning how the [SwissCovid](https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html#-2097806982) mobile application actually works.

* `logger.py`: prints Exposure Notification packets received using BLE in JSON

## Requirements

* Python 3

```console
$ sudo apt install python3-bluez
```

Tested on a Raspberry Pi 3 Model B+ running Raspbian GNU/Linux 10 (buster).
