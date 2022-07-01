from shutil import copyfile
from ui.layouts.Ui_AddTTSDialog import Ui_AddFromTTS
from ui.hotkey_scan_button import HotkeyScanPushButton
from ui.utility_popup_box import MessageBoxesInterface
from PySide2.QtWidgets import (
    QDialog
)
from src.audio_hotkey import AudioHotkey
from src.constants import DEFAULT_CUSTOM_FOLDER, TEMP_TTS_FILE

SHORT_NAME_LEN = 35


class AddCurrentTTSDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent, hotkey_list, last_tts_lang, last_tts_prompt, page) -> None:
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

        # Set default name, if TTS text was preserved
        if last_tts_prompt:
            self._ui.leName.setText(
                f"[{last_tts_lang}] {last_tts_prompt[0:min(len(last_tts_prompt), SHORT_NAME_LEN)]}")

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
