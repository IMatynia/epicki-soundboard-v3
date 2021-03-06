import sounddevice

_DEVICE_LIST = list(sounddevice.query_devices())


class InvalidDeviceNameError(Exception):
    def __init__(self, d_name) -> None:
        super().__init__(f"Device with name {d_name} not found")


def get_device_number(device_name):
    """Returns present device ID based on device name

    Args:
        device_name (str): device name

    Raises:
        InvalidDeviceName: when the device is not found

    Returns:
        int: device id
    """
    for i, device in enumerate(get_devices()):
        if device["name"] == device_name:
            return i
    raise InvalidDeviceNameError(device_name)


def get_devices_supporting_stereo_output():
    """Returns a dict of id -> device pairs of devices supporting setero output and have valid hostapi

    Returns:
        dict: the id->device pairs
    """
    out = {}
    for i, device in enumerate(get_devices()):
        if device["max_input_channels"] == 0 and device["max_output_channels"] >= 2 and device["hostapi"] == 0:
            out[i] = device
    return out


def get_devices():
    """Returns all available devices (cached)

    Returns:
        list: device list
    """
    return _DEVICE_LIST
