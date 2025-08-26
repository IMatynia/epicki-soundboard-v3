from contextlib import contextmanager
import logging
from pathlib import Path
from threading import Semaphore
from pydantic import BaseModel, Field
from enum import Enum


class SupportedPlaybackFormats(str, Enum):
    mp3 = "mp3"
    wav = "wav"
    ogg = "ogg"


class KeyPress(BaseModel, frozen=True):
    name: str
    vk: int

    @classmethod
    def new(cls, name: str, vk: int):
        return KeyPress(name=name, vk=vk)


class Hotkey(BaseModel, frozen=True):
    keys: set[KeyPress]

    def check_collision(self, other: "Hotkey"):
        return self.keys == other.keys


class AppAudioConfig(BaseModel):
    main_device_on: bool = True
    only_one_sound_at_once: bool = False
    volume_multiplier: float = 1.0
    volume_multiplier_base: float = 1.25
    additional_device_id: str | None = None
    audio_cache_location: Path = Path("./.audio_cache")
    prefered_universal_format: SupportedPlaybackFormats = SupportedPlaybackFormats.mp3

    def get_tts_cache_folder(self):
        path = self.audio_cache_location / "tts"
        path.mkdir(exist_ok=True, parents=True)
        return path

    def get_tts_temporary_file_path(self):
        return (
            self.get_tts_cache_folder()
            / f".tts_cache.{self.prefered_universal_format.value}"
        )

    def get_download_cache_folder(self):
        path = self.audio_cache_location / "downloads"
        path.mkdir(exist_ok=True, parents=True)
        return path

    def get_download_cache_file_by_name(self, name: str) -> Path:
        path = self.audio_cache_location / "downloads" / f"{name}.{self.prefered_universal_format.value}"
        path.parent.mkdir(exist_ok=True, parents=True)
        return path


class AppTTSConfig(BaseModel):
    language: str = "en"
    prompt: str = ""


class AppHotkeys(BaseModel):
    toggle_main_device_playback: Hotkey = Field(
        Hotkey(keys={KeyPress.new("/", 111), KeyPress.new("-", 109)}),
        description="""Toggles playback on the main device""",
    )
    toggle_singular_playback: Hotkey = Field(
        Hotkey(keys={KeyPress.new("/", 111), KeyPress.new("*", 106)}),
        description="""Toggles if only one sound can play at once""",
    )
    increase_volume: Hotkey = Field(
        Hotkey(keys={KeyPress.new("*", 106), KeyPress.new("+", 107)}),
        description="""Increases volume""",
    )
    decrease_volume: Hotkey = Field(
        Hotkey(keys={KeyPress.new("*", 106), KeyPress.new("-", 109)}),
        description="""Decreases volume""",
    )
    stop_all_sounds: Hotkey = Field(
        Hotkey(keys={KeyPress.new("End", 35)}),
        description="""Stops all playing sounds""",
    )
    play_cached_tts: Hotkey = Field(
        Hotkey(keys={KeyPress.new("[", 219)}), description="""Plays saved TTS audio"""
    )
    open_tts_manager: Hotkey = Field(
        Hotkey(keys={KeyPress.new("]", 221)}), description="""Opens TTS manager"""
    )
    next_page: Hotkey = Field(
        Hotkey(keys={KeyPress.new("page_up", 33)}),
        description="""Switches to the next page""",
    )
    previous_page: Hotkey = Field(
        Hotkey(keys={KeyPress.new("page_down", 34)}),
        description="""Switches to the previous page""",
    )

    @classmethod
    def get_all_hotkeys_as_attributes(cls):
        for field_name, field in cls.model_fields.items():
            yield field_name, field.description

class AppSoundboardHotkey(BaseModel):
    page: int
    hotkey: Hotkey
    filename: Path


class AppYTDLPConfig(BaseModel):
    bin_path: str = "yt-dlp"
    extra_arguments: list[str] = Field(default_factory=list)


class AppConfig(BaseModel):
    config_version: str = "3.1.0"
    window_h_pos: int = 200
    window_v_pos: int = 200

    youtube_dl: AppYTDLPConfig = Field(default_factory=AppYTDLPConfig)
    audio_config: AppAudioConfig = Field(default_factory=AppAudioConfig)
    tts_config: AppTTSConfig = Field(default_factory=AppTTSConfig)
    app_hotkeys: AppHotkeys = Field(default_factory=AppHotkeys)
    soundboard_hotkeys: list[AppSoundboardHotkey] = Field(default_factory=list)

    def add_soundboard_hotkey(self, new_hotkey: AppSoundboardHotkey):
        self.soundboard_hotkeys.append(new_hotkey)

    def remove_soundboard_hotkey(self, hotkey_to_remove: AppSoundboardHotkey):
        self.soundboard_hotkeys.remove(hotkey_to_remove)

    def get_soundboard_by_page(self, page_index: int) -> list[AppSoundboardHotkey]:
        return list(filter(lambda x: x.page == page_index, self.soundboard_hotkeys))

    def check_for_collisions(self, hotkey: Hotkey, page: int) -> bool:
        # CHECK PER PAGE
        for hk in self.soundboard_hotkeys:
            if hk.page == page and hk.hotkey.check_collision(hotkey):
                return True
        return False


class ConfigWrapper:
    """Thread safe config wrapper"""

    _config: AppConfig
    _mutex: Semaphore

    def __init__(self) -> None:
        self._config = AppConfig()
        self._mutex = Semaphore()

    def set(self, new: AppConfig):
        with self._mutex:
            self._config = new

    @contextmanager
    def get(self):
        # with self._mutex:
        logging.debug("Config mutex LOCK")
        yield self._config
        logging.debug("Config mutex FREE")

    def toggle_play_on_main(self):
        with self._mutex:
            self._config.audio_config.main_device_on ^= True

    def toggle_singular_playback(self):
        with self._mutex:
            self._config.audio_config.only_one_sound_at_once ^= True

    def decrease_volume(self):
        with self._mutex:
            self._config.audio_config.volume_multiplier /= (
                self._config.audio_config.volume_multiplier_base
            )

    def increase_volume(self):
        with self._mutex:
            self._config.audio_config.volume_multiplier *= (
                self._config.audio_config.volume_multiplier_base
            )
