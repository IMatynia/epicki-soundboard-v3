from PySide2.QtWidgets import (
    QPushButton
)
from src.hotkey_scanner import HotkeyScanner


class HotkeyScanPushButton(QPushButton):
    DEFAULT_TEXT = "Set keys"

    def __init__(self, parent) -> None:
        super().__init__(HotkeyScanPushButton.DEFAULT_TEXT, parent)
        self._keys = set()

        self.clicked.connect(self.on_click)

    def get_keys(self):
        return self._keys

    def on_click(self):
        pass

    def on_hotkey_scan_begin(self):
        self._ui.bScanKeys.setText("Press ESC to stop")
        self.setDisabled(True)
        t_scan = threading.Thread(target=self.scan_and_put_in_shortcut)
        t_scan.start()

    def on_hotkey_scan_complete(self):
        self.setDisabled(False)
        self._ui.bScanKeys.setText("Try again")
        self.update_hotkey_display()

    def scan_and_put_in_shortcut(self):
        scanned_keys = HotkeyScanner.scan_keys_until_release_all()
        self._hotkey.set_keys(scanned_keys)
        self.on_hotkey_scan_complete()
