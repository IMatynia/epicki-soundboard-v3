from PySide2.QtWidgets import (
    QPushButton, QSizePolicy
)
from src.hotkey_scanner import HotkeyScanner
from src.key import keys_to_string


class HotkeyScanPushButton(QPushButton):
    DEFAULT_TEXT = "Set keys"

    def __init__(self, parent, default_keys=None) -> None:
        super().__init__(HotkeyScanPushButton.DEFAULT_TEXT, parent)
        if default_keys:
            self._keys = default_keys
            self.setText(keys_to_string(self._keys))
        else:
            self._keys = set()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.clicked.connect(self.on_click)

    def get_keys(self):
        return self._keys

    def on_click(self):
        self.on_hotkey_scan_begin()

    def on_hotkey_scan_begin(self):
        self.setText("...")
        self.parent().setDisabled(True)
        scanner = HotkeyScanner(self.on_hotkey_scan_complete)
        scanner.start()

    def on_hotkey_scan_complete(self, keys):
        self.parent().setDisabled(False)
        new_text = keys_to_string(keys)
        new_text = new_text if len(
            new_text) > 0 else HotkeyScanPushButton.DEFAULT_TEXT
        self._keys = keys
        self.setText(new_text)
