import sounddevice

_DEVICE_LIST = list(sounddevice.query_devices())


class InvalidDeviceName(Exception):
    def __init__(self, d_name) -> None:
        super().__init__(f"Device with name {d_name} not found")


def get_device_number(device_name):
    for i, device in enumerate(get_devices()):
        if device["name"] == device_name:
            return i
    raise InvalidDeviceName(device_name)


def get_devices_supporting_stereo_output():
    out = {}
    for i, device in enumerate(get_devices()):
        if device["max_input_channels"] == 0 and device["max_output_channels"] >= 2 and device["hostapi"] == 0:
            out[i] = device
    return out


def get_devices():
    return _DEVICE_LIST
