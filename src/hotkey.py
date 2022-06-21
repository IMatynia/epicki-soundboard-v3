class Hotkey:
    def __init__(self, keys, filename, page):
        assert page >= 0
        self._keys = keys
        self._filename = filename
        self._page = page

    def get_filename(self):
        return self._filename

    def get_keys(self):
        return self._keys

    def get_page(self):
        return self._page

    def set_page(self, page):
        assert page >= 0
        self._page = page

    def __eq__(self, other):
        # There can only be one hotkey with given keys per page
        return self._keys == other.get_keys() and self._page == other.get_page()
