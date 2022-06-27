from logging import info
from src.key import Key

SETTINGS_VERSION = "V1.0"


class MissingConfigFieldError(Exception):
    def __init__(self, field_name) -> None:
        super().__init__(f"Config file is missing field [{field_name}]")


class Settings:
    def __init__(self) -> None:
        # Default values | private variables with prefix _s_ are loaded/saved into the config file
        self._s_additional_device = None
        self._s_additional_device_number = -1
        self._s_window_h_pos = 200
        self._s_window_v_pos = 200
        self._s_main_on = True
        self._s_singular = False

        # Shortcuts, defaults:
        self._s_toggle_main = {Key("/", 111), Key("-", 109)}
        self._s_toggle_singular = {Key("/", 111), Key("*", 106)}
        self._s_loud_up = {Key("*", 106), Key("+", 107)}
        self._s_loud_down = {Key("*", 106), Key("-", 109)}
        self._s_silence = {Key("End", 35)}
        self._s_tts_play = {Key("[", 219)}
        self._s_tts_open_manager = {Key("]", 221)}

        # Not saved:
        self._volume_multiplier = 1.0
        self._current_page = 0

    def load_from_dict(self, dict_data):
        """Loads all the values for "_s_" fields, raises an error if the
        dict doesnt provide the data for a field

        Args:
            dict_data (dict): data to load

        Raises:
            MissingConfigFieldError: if a field is missing from the data
        """
        for key in self.__dict__:
            try:
                key_nicer = key[3::]
                if key[0:3] == "_s_":
                    if isinstance(dict_data[key_nicer], list):
                        # Load hotkey sets
                        out = set()
                        for key_data in dict_data[key_nicer]:
                            new_key = Key()
                            new_key.load_from_dict(key_data)
                            out.add(new_key)
                        self.__setattr__(key, out)
                    else:
                        self.__setattr__(key, dict_data[key_nicer])
            except KeyError:
                raise MissingConfigFieldError(key_nicer)

    def save_to_dict(self):
        """Stores all "_s_" fields in the dict

        Returns:
            dict: key value pairs
        """
        out = {
            "conf-version": SETTINGS_VERSION
        }
        for key in self.__dict__:
            key_nicer = key[3::]
            if key[0:3] == "_s_":
                if isinstance(self.__dict__[key], set):
                    # Save hotkey set
                    out[key_nicer] = [key_obj.save_to_dict()
                                      for key_obj in self.__dict__[key]]
                else:
                    out[key_nicer] = self.__dict__[key]
        return out

    def get_additional_device(self):
        return self._s_additional_device

    def get_additional_device_num(self):
        return self._s_additional_device_number

    def set_additional_device(self, name, id):
        self._s_additional_device = name
        self._s_additional_device_number = id

    def get_window_h_pos(self):
        return self._s_window_h_pos

    def set_window_h_pos(self, y):
        self._s_window_h_pos = y

    def get_window_v_pos(self):
        return self._s_window_v_pos

    def set_window_v_pos(self, x):
        self._s_window_v_pos = x

    def get_play_on_main(self):
        """Should i play the audio on the primary device too?

        Returns:
            bool: the anwser
        """
        return self._s_main_on

    def set_play_on_main(self, value):
        self._s_main_on = bool(value)

    def toggle_play_on_main(self):
        self._s_main_on ^= 1

    def get_is_singular(self):
        """Should i play only one sound at once?

        Returns:
            bool: the anwser
        """
        return self._s_singular

    def set_singular_audio(self, value):
        self._s_singular = bool(value)

    def toggle_singular_audio(self):
        self._s_singular ^= 1

    def get_volume_multiplier(self):
        return self._volume_multiplier

    def modify_volume_multiplier(self, multiplier):
        self._volume_multiplier *= multiplier
        info(f"Volume multiplier changed to {self._volume_multiplier}")

    # :/ not fun
    def get_keys_toggle_main(self):
        return self._s_toggle_main

    def get_keys_toggle_singular(self):
        return self._s_toggle_singular

    def get_keys_loud_up(self):
        return self._s_loud_up

    def get_keys_loud_down(self):
        return self._s_loud_down

    def get_keys_silence(self):
        return self._s_silence

    def get_keys_tts_play(self):
        return self._s_tts_play

    def get_keys_tts_open_manager(self):
        return self._s_tts_open_manager

    def set_keys_toggle_main(self, keys):
        self._s_toggle_main = keys

    def set_keys_toggle_singular(self, keys):
        self._s_toggle_singular = keys

    def set_keys_loud_up(self, keys):
        self._s_loud_up = keys

    def set_keys_loud_down(self, keys):
        self._s_loud_down = keys

    def set_keys_silence(self, keys):
        self._s_silence = keys

    def set_keys_tts_play(self, keys):
        self._s_tts_play = keys

    def set_keys_tts_open_manager(self, keys):
        self._s_tts_open_manager = keys
