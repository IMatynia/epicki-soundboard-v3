from os import remove
import re
from ui.layouts.Ui_YoutubeDialog import Ui_AddYoutubeDL
from ui.utility_popup_box import MessageBoxesInterface
from ui.hotkey_scan_button import HotkeyScanPushButton
from PySide2.QtWidgets import (
    QDialog
)
from src.audio_hotkey import AudioHotkey
import threading
from src.youtube_dl_handle import download_media
from src.ffmpeg_handle import ffmpeg_conversion, FFMPEGRuntimeError
from src.constants import DEFAULT_CUSTOM_FOLDER, TEMP_YTDL_FILE


class AddYoutubeDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent, hotkey_list, page) -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._ui = Ui_AddYoutubeDL()
        self._ui.setupUi(self)
        self._hotkey = AudioHotkey(None, None, page)
        self._hotkey_list = hotkey_list

        # Set up triggers
        self._scan_button = HotkeyScanPushButton(self)
        self._ui.buttonPlaceholder.addWidget(self._scan_button)
        self._ui.bSave.clicked.connect(self.on_save_begin)
        self._ui.bCancel.clicked.connect(self.reject)

    def on_save_begin(self):
        custom_name = self._ui.leName.text()
        url = self._ui.leURL.text()

        ytdl_args = self._ui.leYTDLargs.text().split(" ")
        ffmpeg_args = self._ui.leFFMPEGargs.text().split(" ")

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
            self.setDisabled(True)
            th = threading.Thread(
                target=self.get_media_async_with_updates, args=[url, filename, ytdl_args, ffmpeg_args])
            th.start()

    def set_status(self, prompt, percentage):
        self._ui.lStatus.setText(prompt)
        self._ui.progressBar.setValue(percentage)

    def get_media_async_with_updates(self, url, destination, ytdl_args, ffmpeg_args):
        self.set_status("Starting download", 0)

        def callback(line):
            matches = re.findall("\\ [1234567890\.]*%", line)
            if len(matches) > 0:
                percentage = float(matches[0][1:-1])*0.9
                self.set_status("Downloading media via YT-DL", percentage)

        # Download mp3 via YT-DL
        download_media(url, TEMP_YTDL_FILE, ytdl_args, callback)
        # Download finished, FFMPEG conversion
        self.set_status("Converting to OGG via FFMPEG", 95.0)
        ret_val = ffmpeg_conversion(TEMP_YTDL_FILE, destination, ffmpeg_args)
        if not ret_val == 0:
            raise FFMPEGRuntimeError() 
        remove(TEMP_YTDL_FILE)
        self.on_save_complete()

    def on_save_complete(self):
        self.accept()

    def get_hotkey(self):
        return self._hotkey
