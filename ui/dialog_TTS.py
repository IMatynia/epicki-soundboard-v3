from shutil import copyfile
from ui.layouts.Ui_TTSDialog import Ui_AddFromTTS
from PySide2.QtWidgets import (
    QDialog
)
from src.audio_hotkey import AudioHotkey
import threading
from src.keyboard_hotkeys import keys_to_string, HotkeyScanner
from src.constants import DEFAULT_CUSTOM_FOLDER, TEMP_TTS_FILE


class AddCurrentTTS(QDialog):
    def __init__(self, parent, hotkey_list, page) -> None:
        super().__init__(parent)
        self._ui = Ui_AddFromTTS()
        self._ui.setupUi(self)
        self._hotkey = AudioHotkey(None, None, page)
        self._hotkey_list = hotkey_list

        self._ui.bScanKeys.clicked.connect(self.on_hotkey_scan_begin)
        self._ui.bSave.clicked.connect(self.on_save_begin)
        self._ui.bCancel.clicked.connect(self.reject)

    def on_hotkey_scan_begin(self):
        self._ui.bScanKeys.setText("Press ESC to stop")
        self.setDisabled(True)
        t_scan = threading.Thread(target=self.scan_and_put_in_shortcut)
        t_scan.start()

    def on_hotkey_scan_complete(self):
        self.setDisabled(False)
        self._ui.bScanKeys.setText("Try again")
        self.update_hotkey_display()

    def on_save_begin(self):
        custom_name = self._ui.leName.text()

        filename = f"{DEFAULT_CUSTOM_FOLDER}/{custom_name}.ogg"
        self._hotkey.set_filename(filename)

        if self._hotkey.get_keys() is None or len(self._hotkey.get_keys()) == 0:
            # No keys
            self.show_popup("Keys cant be empty!")

        elif self._hotkey_list.check_collision(self._hotkey):
            # Collision
            self.show_popup(
                "This hotkey colides with another one on this page!")
        else:
            copyfile(TEMP_TTS_FILE, filename)
            self.accept()

    def update_hotkey_display(self):
        text = keys_to_string(self._hotkey.get_keys())
        text = text if not text == "" else "Awaiting input"
        self._ui.lKeys.setText(text)

    def get_hotkey(self):
        return self._hotkey

    def scan_and_put_in_shortcut(self):
        scanned_keys = HotkeyScanner.scan_keys_until_release_all()
        self._hotkey.set_keys(scanned_keys)
        self.on_hotkey_scan_complete()
