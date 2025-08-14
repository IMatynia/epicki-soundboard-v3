"""Separation of responsibilities - why does an audio playing thread also add itself to a thread pool and holds a static reference"""

from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
import sounddevice
import soundfile
import threading
import numpy as np
from logging import info
from os import path
from contextlib import contextmanager


BLOCK_SIZE = 1024


class InvalidDeviceIDError(Exception):
    def __init__(self, id: "int") -> None:
        super().__init__(f"Device of id {id} is invalid!")


class MultiAudioPlayThread(threading.Thread):
    """Works as a sound file playing thread. Use .start() to make
    it run, and .stop_this() to stop at any point. Works with ogg and wav files.
    Plays the file on 1 or 2 devices, as described in settings.
    """

    def __init__(self, audio_file: Path, device_id: str | None):
        super().__init__(daemon=True)
        self._running = True
        self._audio_file = audio_file
        self._device_id = device_id or "DEFAULT"
        self._device_number = (
            AudioPlaybackProvider.get_device_number(device_id) if device_id else None
        )

        if not path.exists(self._audio_file):
            raise FileNotFoundError()

    @staticmethod
    @contextmanager
    def device_guard(device_stream: sounddevice.OutputStream):
        device_stream.start()
        yield device_stream
        device_stream.stop()
        device_stream.close()

    def run(self):
        with soundfile.SoundFile(self._audio_file) as sound_data:
            with self.device_guard(
                sounddevice.OutputStream(
                    samplerate=sound_data.samplerate,
                    dtype="float32",
                    channels=sound_data.channels,
                    device=self._device_number,
                )
            ) as device_stream:
                info(
                    f"Now playing {self._audio_file} ({sound_data.frames / sound_data.samplerate: 0.2f} s) on device {self._device_id}"
                )

                for block in sound_data.blocks(blocksize=BLOCK_SIZE, dtype="float32"):
                    processed_block = AudioPlaybackProvider.audio_processor(block)
                    device_stream.write(processed_block)

                    if not self._running:
                        break

    def stop_this(self):
        info(f"Stopping sound on {self.name}")
        self._running = False


class Device(BaseModel):
    index: int
    name: str
    hostapi: int
    max_input_channels: int
    max_output_channels: int
    default_low_input_latency: float
    default_low_output_latency: float
    default_high_input_latency: float
    default_high_output_latency: float
    default_samplerate: float


class AudioPlaybackProvider:
    _playback_threads: list[MultiAudioPlayThread] = []
    _volume: float = 1.0

    @classmethod
    def audio_processor(cls, audio_block):
        """Post processes the audio before it arrives at audio stream.
        For the time being all it does is multiplied the volume by a
        multiplier from settings
        """
        block = np.empty_like(audio_block)
        block[:] = audio_block
        block *= cls._volume
        return block

    @classmethod
    @lru_cache
    def get_all_devices(cls) -> list[Device]:
        out: list[Device] = []
        for device in sounddevice.query_devices():
            out.append(Device.model_validate(device))
        return out

    @classmethod
    def get_device_number(cls, device_id: str) -> int: ...

    @classmethod
    def stop_all_sounds(cls):
        """Stops all running audio threads."""
        for thread in cls._playback_threads:
            thread.stop_this()
        cls._playback_threads = []

    @classmethod
    def _play_audio_non_blocking(
        cls, audio_file: Path, device_id: str | None = None
    ) -> "MultiAudioPlayThread":
        """Non blocking audio playback. Stop it by calling .stop_this on the thread or stop_all_sounds on playback provider"""
        th = MultiAudioPlayThread(audio_file, device_id)
        th.start()
        cls._playback_threads.append(th)
        return th

    @classmethod
    def play_audio_non_blocking_main_and_additional(
        cls, audio_file: Path, device_id: str, singular: bool, play_on_main: bool
    ):
        if singular:
            cls.stop_all_sounds()

        cls._play_audio_non_blocking(audio_file, device_id)
        if play_on_main:
            cls._play_audio_non_blocking(audio_file)
