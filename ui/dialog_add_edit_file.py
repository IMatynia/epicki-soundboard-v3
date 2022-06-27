from ui.layouts.Ui_AddEditFileDialog import Ui_AddEditFileDialog
from ui.hotkey_scan_button import HotkeyScanPushButton
from ui.utility_popup_box import MessageBoxesInterface
from PySide2.QtWidgets import (
    QDialog, QFileDialog
)
from src.audio_hotkey import AudioHotkey
from src.key import keys_to_string
from src.ffmpeg_handle import ffmpeg_conversion
from src.utils import check_if_program_present_in_path
from os import path
import threading
from logging import info


class AddEditFileDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent, hotkey_list, page, keys=None, file=None) -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._ui = Ui_AddEditFileDialog()
        self._ui.setupUi(self)
        self._hotkey = AudioHotkey(keys, file, page)
        self._hotkey_list = hotkey_list

        if file:
            self.update_file_display()

        # Set up triggers
        self._scan_button = HotkeyScanPushButton(self, keys)
        self._ui.buttonPlaceholder.addWidget(self._scan_button)
        self._ui.bChooseFile.clicked.connect(self.on_file_select)
        self._ui.bSave.clicked.connect(self.on_save)
        self._ui.bCancel.clicked.connect(self.reject)

    def on_file_select(self):
        file_dialog = QFileDialog(self)
        file = file_dialog.getOpenFileName(
            caption="Choose a media file",
        )[0]

        if not file:
            info("No file chosen")
        else:
            self._hotkey.set_filename(file)
            self.update_file_display()

    def on_save(self):
        filename = self._ui.leFilePath.text()
        self._hotkey.set_filename(filename)
        self._hotkey.set_keys(self._scan_button.get_keys())

        self.setDisabled(True)
        if not path.exists(filename):
            # File does not exist
            self.show_popup("Invalid file!")
        elif self._hotkey.get_keys() is None or len(self._hotkey.get_keys()) == 0:
            # No keys
            self.show_popup("Keys cant be empty!")
        elif self._hotkey_list.check_collision(self._hotkey):
            # Collision
            self.show_popup(
                "This hotkey colides with another one on this page!")
        elif filename.split(".")[-1] not in set(["ogg", "wav"]):
            # Invalid data type
            if check_if_program_present_in_path("ffmpeg"):
                # Try to use ffmpeg

                choice = self.show_choice(
                    "Do you want to automatically convert this media into OGG using ffmpeg? (Create a copy in OGG format)")
                if choice:
                    # Convert the media into ogg (or at least try, let ffmpeg handle it)
                    ogg_filename = ".".join(filename.split(".")[0:-1]) + ".ogg"
                    info(f"Converting {filename} to {ogg_filename}")
                    ffmpeg_conversion(filename, ogg_filename)
                    self._hotkey.set_filename(ogg_filename)
                    self.accept()
            else:
                # No ffmpeg available
                self.show_popup(
                    "This file format is not supported. Add FFMPEG to PATH to automatically convert")
        else:
            self.accept()
        self.setDisabled(False)

    def update_file_display(self):
        text = self._hotkey.get_filename()
        self._ui.leFilePath.setText(text)

    def get_hotkey(self):
        return self._hotkey