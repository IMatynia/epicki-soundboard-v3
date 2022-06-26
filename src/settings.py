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

        # Shortcuts: TODO: change format
        self._s_toggle_main = "*|/"
        self._s_toggle_singular = "-|/"
        self._s_loud_up = "*|+"
        self._s_loud_down = "*|-"
        self._s_silence = "End"
        self._s_tts_play = "]"

        # Not saved:
        self._loudness_multiplier = 1.0
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
                if key[0:3] == "_s_":
                    self.__setattr__(key, dict_data[key[3::]])
            except KeyError:
                raise MissingConfigFieldError(key[3::])

    def save_to_dict(self):
        """Stores all "_s_" fields in the dict

        Returns:
            dict: key value pairs
        """
        out = {
            "conf-version": SETTINGS_VERSION
        }
        for key in self.__dict__:
            if key[0:3] == "_s_":
                out[key[3::]] = self.__dict__[key]
        return out

    def get_additional_device(self):
        return self._s_additional_device

    def get_additional_device_num(self):
        return self._s_additional_device_number

    def get_window_h_pos(self):
        return self._s_window_h_pos

    def get_window_v_pos(self):
        return self._s_window_v_pos

    def get_play_on_main(self):
        """Should i play the audio on the primary device too?

        Returns:
            bool: the anwser
        """
        return self._s_main_on

    def get_is_singular(self):
        """Should i play only one sound at once?

        Returns:
            bool: the anwser
        """
        return self._s_singular

    def get_loudness(self):
        return self._loudness_multiplier

    def set_additional_device(self, name, id):
        self._s_additional_device = name
        self._s_additional_device_number = id

    def set_play_on_main(self, value):
        assert isinstance(value, bool)
        self._s_main_on = value
