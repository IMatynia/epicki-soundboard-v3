from os import remove
import re
from ui.layouts.Ui_YoutubeDialog import Ui_AddYoutubeDL
from PySide2.QtWidgets import (
    QDialog, QMessageBox
)
from src.audio_hotkey import AudioHotkey
import threading
from src.hotkey_reader import scan_pressed_keys
from src.youtube_dl_handle import download_media
from src.ffmpeg_handle import ffmpeg_conversion
from src.constants import DEFAULT_CUSTOM_FOLDER, TEMP_YTDL_FILE


class AddYoutubeDialog(QDialog):
    def __init__(self, parent, hotkey_list, page) -> None:
        super().__init__(parent)
        self._ui = Ui_AddYoutubeDL()
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
        url = self._ui.leURL.text()
        # WIP TODO:
        filename = f"{DEFAULT_CUSTOM_FOLDER}/{custom_name}.ogg"
        self._hotkey.set_filename(filename)

        err_box = QMessageBox(self)
        if self._hotkey.get_keys() is None or len(self._hotkey.get_keys()) == 0:
            # No keys
            err_box.setText(
                "Keys cant be empty!")
            err_box.show()
        elif self._hotkey_list.check_collision(self._hotkey):
            # Collision
            err_box.setText(
                "This hotkey colides with another one on this page!")
            err_box.show()
        else:
            self.setDisabled(True)
            th = threading.Thread(
                target=self.get_media_async, args=[url, filename])
            th.start()

    def set_status(self, prompt, percentage):
        self._ui.lStatus.setText(prompt)
        self._ui.progressBar.setValue(percentage)

    def get_media_async(self, url, destination):
        self.set_status("Starting download", 0)

        def callback(line):
            matches = re.findall("\ [1234567890\.]*%", line)
            if len(matches) > 0:
                percentage = float(matches[0][1:-1])*0.9
                self.set_status("Downloading media via YT-DL", percentage)

        # Download mp3 via YT-DL
        download_media(url, TEMP_YTDL_FILE, callback)
        # Download finished, FFMPEG conversion
        self.set_status("Converting to OGG via FFMPEG", 95.0)
        ffmpeg_conversion(TEMP_YTDL_FILE, destination)
        remove(TEMP_YTDL_FILE)
        self.on_save_complete()

    def on_save_complete(self):
        self.accept()

    def update_hotkey_display(self):
        text = " + ".join(self._hotkey.get_keys())
        text = text if not text == "" else "Awaiting input"
        self._ui.lKeys.setText(text)

    def get_hotkey(self):
        return self._hotkey

    def scan_and_put_in_shortcut(self):
        scanned_keys = scan_pressed_keys()
        self._hotkey.set_keys(scanned_keys)
        self.on_hotkey_scan_complete()
