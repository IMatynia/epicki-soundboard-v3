from shutil import copyfile
from ui.layouts.Ui_AddTTSDialog import Ui_AddFromTTS
from ui.hotkey_scan_button import HotkeyScanPushButton
from ui.utility_popup_box import MessageBoxesSimple
from PySide6.QtWidgets import QDialog
from src.config.config import AppSoundboardHotkey, AppConfig, Hotkey

SHORT_NAME_LEN = 35


class AddCurrentTTSDialog(QDialog):
    def __init__(self, parent, conifg: AppConfig, current_page: int) -> None:
        super().__init__(parent)
        self._ui = Ui_AddFromTTS()
        self._ui.setupUi(self)
        self._msg = MessageBoxesSimple(self)
        self._config = conifg

        # Set up triggers
        self._scan_button = HotkeyScanPushButton(self)
        self._ui.buttonPlaceholder.addWidget(self._scan_button)
        self._ui.bSave.clicked.connect(self.on_save)
        self._ui.bCancel.clicked.connect(self.reject)
        self._hotkey = None
        self._page = current_page

        # Set default name, if TTS text was preserved
        last_prompt = self._config.tts_config.prompt
        lang = self._config.tts_config.language

        self._ui.leName.setText(
            f"[{lang}] {last_prompt[0 : min(len(last_prompt), SHORT_NAME_LEN)]}"
        )

    def on_save(self):
        custom_name = self._ui.leName.text()
        scanned_keys = self._scan_button.get_keys()
        if scanned_keys is None or len(scanned_keys) == 0:
            # No keys
            self._msg.show_popup("Keys cant be empty!")
            return
        hotkey = Hotkey(keys=scanned_keys)

        tts_temp_file = self._config.audio_config.get_tts_temporary_file_path()
        tts_cache_folder = self._config.audio_config.get_tts_cache_folder()
        prefered_format = self._config.audio_config.prefered_universal_format

        if self._config.check_for_collisions(hotkey, self._page):
            self._msg.show_popup("This hotkey colides with another one on this page!")
            return

        result_path = tts_cache_folder / f"{custom_name}.{prefered_format.value}"

        try:
            copyfile(tts_temp_file, result_path)
            self._hotkey = AppSoundboardHotkey(
                page=self._page, hotkey=hotkey, filename=result_path
            )
            self.accept()
        except OSError:
            self._msg.show_popup(f"Filename {result_path} is not allowed!")

    def accept(self) -> None:
        if self._hotkey:
            self._config.add_soundboard_hotkey(self._hotkey)
        return super().accept()
