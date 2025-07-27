from pathlib import Path
from pydantic import BaseModel, Field
import chemical


class KeyPress(BaseModel, frozen=True):
    name: str
    vk: int

    @classmethod
    def new(cls, name: str, vk: int):
        return KeyPress(name=name, vk=vk)


class Hotkey(BaseModel, frozen=True):
    keys: set[KeyPress]


class AppAudioConfig(BaseModel):
    main_device_on: bool = True
    only_one_sound_at_once: bool = False
    volume_multiplier: float = 1.0
    volume_multiplier_base: float = 1.25
    additional_device_id: str | None = None
    audio_cache_location: Path = Path("./.audio_cache")


class AppTTSConfig(BaseModel):
    language: str = "en"
    prompt: str = ""


class AppHotkeys(BaseModel):
    toggle_main_device_playback: Hotkey = Hotkey(
        keys={KeyPress.new("/", 111), KeyPress.new("-", 109)}
    )
    toggle_singular_playback: Hotkey = Hotkey(
        keys={KeyPress.new("/", 111), KeyPress.new("*", 106)}
    )
    increase_volume: Hotkey = Hotkey(
        keys={KeyPress.new("*", 106), KeyPress.new("+", 107)}
    )
    decrease_volume: Hotkey = Hotkey(
        keys={KeyPress.new("*", 106), KeyPress.new("-", 109)}
    )
    stop_all_sounds: Hotkey = Hotkey(keys={KeyPress.new("End", 35)})
    play_cached_tts: Hotkey = Hotkey(keys={KeyPress.new("[", 219)})
    open_tts_manager: Hotkey = Hotkey(keys={KeyPress.new("]", 221)})


class AppSoundboardHotkey(BaseModel):
    page: int
    hotkey: Hotkey
    filename: Path


class AppConfig(BaseModel):
    config_version: str = "3.1.0"
    window_h_pos: int = 200
    window_v_pos: int = 200

    audio_config: AppAudioConfig = Field(default_factory=AppAudioConfig)
    tts_config: AppTTSConfig = Field(default_factory=AppTTSConfig)
    app_hotkeys: AppHotkeys = Field(default_factory=AppHotkeys)
    soundboard_hotkeys: list[AppSoundboardHotkey] = Field(default_factory=list)

    def get_soundboard_by_page(self, page_index: int) -> list[AppSoundboardHotkey]:
        return list(filter(lambda x: x.page == page_index, self.soundboard_hotkeys))
