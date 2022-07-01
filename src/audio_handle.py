from src.settings import Settings
from src.audio_devices import get_devices
import sounddevice
import soundfile
import threading
import numpy as np
from logging import info
from os import path

BLOCK_SIZE = 1024


class InvalidDeviceIDError(Exception):
    def __init__(self, id: "int") -> None:
        super().__init__(f"Device of id {id} is invalid!")


class MultiAudioPlayThread(threading.Thread):
    """Works as a sound file playing thread. Use .start() to make 
    it run, and .stop_this() to stop at any point. Works with ogg and wav files.
    Plays the file on 1 or 2 devices, as described in settings.
    """
    _ALL_AUDIO_THREADS = []

    def __init__(self, filename: "str", settings: "Settings", args=(), kwargs=None):
        """Create the mutliaudioplay object.

        Args:
            filename (str): path to audio file
            settings (Settings): settings to pull data from

        Raises:
            FileNotFoundError: if the given file does not exist
        """
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.daemon = True
        self._stopped = False
        self._filename = filename
        self._settings = settings

        if not path.exists(self._filename):
            raise FileNotFoundError()

        MultiAudioPlayThread._ALL_AUDIO_THREADS.append(self)

    def run(self):
        with soundfile.SoundFile(self._filename) as sound_data:
            # Get the right device ID
            invalid_device = False
            additiona_device_number = self._settings.get_additional_device_num()
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
                f"Now playing {self._filename} ({sound_data.frames/sound_data.samplerate : 0.2f} s) on device {self._settings.get_additional_device()}")

            main_device.start()
            secondary_device.start()

            for block in sound_data.blocks(blocksize=BLOCK_SIZE, dtype="float32"):
                processed_block = self._audio_processor(block)
                secondary_device.write(processed_block)
                if self._settings.get_play_on_main() and not invalid_device:
                    main_device.write(processed_block)

                if self._stopped:
                    break

            main_device.stop()
            secondary_device.stop()

            main_device.close()
            secondary_device.close()

    def stop_this(self):
        info(f"Stopping sound on {self.name}")
        self._stopped = True

    def _audio_processor(self, block_raw):
        """Post processes the audio before it arrives at audio stream.
        For the time being all it does is multiplied the volume by a
        multiplier from settings
        """
        block = np.empty_like(block_raw)
        block[:] = block_raw
        block *= self._settings.get_volume_multiplier()
        return block


def stop_all_sounds():
    """Stops all running audio threads.
    """
    for thread in MultiAudioPlayThread._ALL_AUDIO_THREADS:
        thread.stop_this()
    MultiAudioPlayThread._ALL_AUDIO_THREADS = []


def multi_audio_play_async(filename: "str", settings: "Settings") -> "MultiAudioPlayThread":
    """Simple function that initializes the MultiAudioPlayThread and returns it

    Args:
        filename (str): the file to play
        settings (Settings): settings to use

    Returns:
        MultiAudioPlayThread: the started audio thread
    """
    if settings.get_is_singular():
        stop_all_sounds()
    th = MultiAudioPlayThread(filename, settings)
    th.start()
    return th
