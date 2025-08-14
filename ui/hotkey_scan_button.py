from PySide6.QtWidgets import QPushButton, QSizePolicy
from src.config.config import KeyPress
from src.hotkey_scanner import HotkeyScanner


def keys_to_string(keys: set[KeyPress]) -> str:
    return " + ".join(map(lambda x: x.name, keys))


class HotkeyScanPushButton(QPushButton):
    DEFAULT_TEXT = "Set keys"
    _keys: set[KeyPress]
    _scanner: HotkeyScanner | None = None

    def __init__(self, parent, default_keys: set[KeyPress] | None = None) -> None:
        super().__init__(HotkeyScanPushButton.DEFAULT_TEXT, parent)
        if default_keys:
            self._keys = default_keys
            self.setText(keys_to_string(self._keys))
        else:
            self._keys = set()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.clicked.connect(self.on_hotkey_scan_begin)

    def get_keys(self):
        if len(self._keys) == 0:
            return None
        return self._keys

    def on_hotkey_scan_begin(self):
        self.setText("...")
        self.parent().setDisabled(True)  # type: ignore
        self._scanner = HotkeyScanner(self.on_hotkey_scan_complete)
        self._scanner.start()

    def on_hotkey_scan_complete(self, keys):
        self.parent().setDisabled(False)  # type: ignore
        new_text = keys_to_string(keys)
        new_text = new_text if len(new_text) > 0 else HotkeyScanPushButton.DEFAULT_TEXT
        self._keys = keys
        self.setText(new_text)
