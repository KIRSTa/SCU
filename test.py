from dataclasses import dataclass
from typing import List


@dataclass
class UsbDevice:
    Connected: str
    Host: str
    VID: str
    PID: str
    Product: str
    Manufacturer: str
    Serial_Number: str
    Bus_Port: str
    Disconnected: str


def parse_usb_history(usb_devices_text)->List[UsbDevice]:
    data = usb_devices_text.split("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−")[1:]
    devices = []
    for device in data[1:-1]:
        devices.append(
            UsbDevice(
                *[d.split(": ")[-1].replace(" ", "") for d in device[1:-1].split("\n")]
            )
        )

    return devices


devices = parse_usb_history()

# d2 = devices[1]
# print(d2.PID)

# for device in devices:
#     print(f'Product: {device.Product}, PID: {device.PID}')

# a = ["a","a","a","a","a","a","a","a","b"]


# print(len(devices))
# print(devices[0].Product)
# # for device in devices:
#     # print(device.Product)
