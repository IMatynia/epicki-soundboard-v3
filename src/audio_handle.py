from src.settings import Settings
import sounddevice
import soundfile
import threading
import numpy as np
from logging import info

_DEVICE_LIST = list(sounddevice.query_devices())
_ALL_AUDIO_THREADS = []
BLOCK_SIZE = 1024


class InvalidDeviceIDError(Exception):
    def __init__(self, id) -> None:
        super().__init__(f"Device of id {id} is invalid!")


class MultiAudioPlayThread(threading.Thread):
    def __init__(self, filename, options: "Settings", args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.daemon = True
        self._stopped = False
        self._filename = filename
        self._options = options

        _ALL_AUDIO_THREADS.append(self)

    def run(self):
        with soundfile.SoundFile(self._filename) as sound_data:
            # Get the right device ID
            invalid_device = False
            additiona_device_number = self._options.get_additional_device_num()
            if additiona_device_number < 0 or additiona_device_number >= len(get_devices()):
                info("Invalid device id, playing on default device!")
                additiona_device_number = sounddevice.default.device
                invalid_device = True

            main_device = sounddevice.OutputStream(samplerate=sound_data.samplerate,
                                                   dtype="float32",
                                                   channels=sound_data.channels)
            secondary_device = sounddevice.OutputStream(samplerate=sound_data.samplerate,
                                                        dtype="float32",
                                                        channels=sound_data.channels,
                                                        device=additiona_device_number)
            info(
                f"Now playing {self._filename} ({sound_data.frames/sound_data.samplerate : 0.2f} s) on device {self._options.get_additional_device()}")

            main_device.start()
            secondary_device.start()

            for block in sound_data.blocks(blocksize=BLOCK_SIZE, dtype="float32"):
                processed_block = self.audio_processor(block)
                secondary_device.write(processed_block)
                if self._options.get_play_on_main() and not invalid_device:
                    main_device.write(processed_block)

                if self._stopped:
                    break

            main_device.stop()
            secondary_device.stop()

            main_device.close()
            secondary_device.close()

    def stop_this(self):
        info(f"Stopping sound on thread {self.name}")
        self._stopped = True

    def audio_processor(self, block_raw):
        block = np.empty_like(block_raw)
        block[:] = block_raw
        block *= self._options.get_loudness()
        return block


def stop_all_sounds():
    global _ALL_AUDIO_THREADS
    for thread in _ALL_AUDIO_THREADS:
        thread.stop_this()
    _ALL_AUDIO_THREADS = []


def get_device_number(device):
    return _DEVICE_LIST.index(device)


def get_devices_supporting_stereo_output():
    out = []
    for device in get_devices():
        if device["max_input_channels"] == 0 and device["max_output_channels"] >= 2:
            out.append(device)


def get_devices():
    return _DEVICE_LIST
