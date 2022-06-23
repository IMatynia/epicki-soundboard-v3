
def make_hotkey_from_dict(dict):
    return AudioHotkey(
        set(dict["keys"]),
        dict["filename"],
        dict["page"]
    )


class AudioHotkey:
    def __init__(self, keys=None, filename=None, page=None):
        """Creates an instance of soundboard hotkey

        Args:
            keys (set): a set of pressed named keys
            filename (str): the audio file to play
            page (int): page number where the hotkey is located
        """
        assert page is None or page >= 0
        self._keys = keys
        self._filename = filename
        self._page = page

    def get_filename(self):
        return self._filename

    def set_filename(self, new_file):
        self._filename = new_file

    def get_keys(self):
        return self._keys

    def set_keys(self, new_keys):
        self._keys = new_keys

    def get_page(self):
        return self._page

    def set_page(self, page):
        assert page >= 0
        self._page = page

    def __hash__(self) -> int:
        return hash(self._page) + hash("".join(sorted(list(self._keys))))

    def __eq__(self, other):
        # There can only be one hotkey with given keys per page
        return self._keys == other.get_keys() and self._page == other.get_page()

    def __str__(self) -> str:
        return f"Hotkey {self._keys} activating file {self._filename}"

    def save_as_dict(self):
        return {
            "keys": list(self._keys),
            "filename": self._filename,
            "page": self._page
        }


class HotkeyCollisionError(Exception):
    def __init__(self, hotkey) -> None:
        super().__init__(
            f"Hotkey [{hotkey}] collides with another one on the page")


class AudioHotkeyList:
    def __init__(self, max_size=256) -> None:
        self._max_size = max_size
        self._pages = [list() for i in range(max_size)]

    def add_hotkey(self, hotkey):
        if self.check_collision(hotkey):
            raise HotkeyCollisionError(hotkey)
        self._pages[hotkey.get_page()].append(hotkey)

    def get_page(self, page_number):
        return self._pages[page_number]

    def get_max_pages(self):
        return self._max_size

    def remove_hotkey(self, hotkey):
        self._pages[hotkey.get_page()].remove(hotkey)

    def check_collision(self, hotkey):
        return hotkey in self._pages[hotkey.get_page()]

    def purge_data(self):
        self._pages = [list() for i in range(self._max_size)]

    def load_from_list(self, list):
        self.purge_data()
        for hotkey_data in list:
            self.add_hotkey(make_hotkey_from_dict(hotkey_data))

    def save_to_list(self):
        out = []
        for page in self._pages:
            out.extend([hotkey.save_as_dict() for hotkey in page])
        return out
