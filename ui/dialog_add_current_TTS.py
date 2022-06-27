from shutil import copyfile
from ui.layouts.Ui_TTSDialog import Ui_AddFromTTS
from ui.hotkey_scan_button import HotkeyScanPushButton
from ui.utility_popup_box import MessageBoxesInterface
from PySide2.QtWidgets import (
    QDialog
)
from src.audio_hotkey import AudioHotkey
from src.constants import DEFAULT_CUSTOM_FOLDER, TEMP_TTS_FILE


class AddCurrentTTSDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent, hotkey_list, page) -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._ui = Ui_AddFromTTS()
        self._ui.setupUi(self)
        self._hotkey = AudioHotkey(None, None, page)
        self._hotkey_list = hotkey_list

        # Set up triggers
        self._scan_button = HotkeyScanPushButton(self)
        self._ui.buttonPlaceholder.addWidget(self._scan_button)
        self._ui.bSave.clicked.connect(self.on_save)
        self._ui.bCancel.clicked.connect(self.reject)

    def on_save(self):
        custom_name = self._ui.leName.text()

        filename = f"{DEFAULT_CUSTOM_FOLDER}/{custom_name}.ogg"
        self._hotkey.set_filename(filename)
        self._hotkey.set_keys(self._scan_button.get_keys())

        if self._hotkey.get_keys() is None or len(self._hotkey.get_keys()) == 0:
            # No keys
            self.show_popup("Keys cant be empty!")

        elif self._hotkey_list.check_collision(self._hotkey):
            # Collision
            self.show_popup(
                "This hotkey colides with another one on this page!")
        else:
            try:
                copyfile(TEMP_TTS_FILE, filename)
                self.accept()
            except OSError:
                self.show_popup(f"Filename {filename} is not allowed!")

    def get_hotkey(self):
        return self._hotkey
