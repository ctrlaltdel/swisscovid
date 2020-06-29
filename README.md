# SwissCovid learning tools

Tools for learning how the [SwissCovid](https://www.bag.admin.ch/bag/en/home/krankheiten/ausbrueche-epidemien-pandemien/aktuelle-ausbrueche-epidemien/novel-cov/situation-schweiz-und-international.html#-2097806982) mobile application actually works.

* `logger.py`: prints Exposure Notification packets received using BLE in JSON
* `exposed.py`: prints exposure records from the API

## Requirements

* Python 3

```console
$ sudo apt install python3-bluez
```

Tested on a Raspberry Pi 3 Model B+ running Raspbian GNU/Linux 10 (buster).

## References

* [Google Exposure Notifications landing page](https://www.google.com/covid19/exposurenotifications/)
* [Exposure Notification - Bluetooth Specification v1.2.2](https://blog.google/documents/70/Exposure_Notification_-_Bluetooth_Specification_v1.2.2.pdf)
* [Specification of the Bluetooth System v5.0](https://www.bluetooth.org/DocMan/handlers/DownloadDoc.ashx?doc_id=421043&_ga=2.29692863.121228451.1498147116-1432843607.1484151012)
