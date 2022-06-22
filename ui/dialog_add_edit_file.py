from ui.layouts.Ui_AddEditFileDialog import Ui_AddEditFileDialog
from PySide2.QtWidgets import (
    QDialog, QFileDialog, QMessageBox
)
from src.hotkey import Hotkey
from src.hotkey_reader import scan_pressed_keys
from src.ffmpeg_handle import ffmpeg_conversion
from src.utils import check_if_program_present_in_path
from os import path
import threading
from logging import info


class AddEditFileDialog(QDialog):
    def __init__(self, parent, hotkey_list, page, keys=None, file=None) -> None:
        super().__init__(parent)
        self._ui = Ui_AddEditFileDialog()
        self._ui.setupUi(self)
        self._hotkey = Hotkey(keys, file, page)
        self._hotkey_list = hotkey_list

        if keys and file:
            self.update_hotkey_display()
            self.update_file_display()

        # Set up triggers
        self._ui.bScanKeys.clicked.connect(self.on_hotkey_scan_begin)
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

    def on_hotkey_scan_begin(self):
        self._ui.bScanKeys.setText("Press ESC to stop")
        self.setDisabled(True)
        t_scan = threading.Thread(target=self.scan_and_put_in_shortcut)
        t_scan.start()

    def on_hotkey_scan_complete(self):
        self.setDisabled(False)
        self._ui.bScanKeys.setText("Try again")
        self.update_hotkey_display()

    def on_save(self):
        filename = self._ui.leFilePath.text()
        self._hotkey.set_filename(filename)

        err_box = QMessageBox(self)
        self.setDisabled(True)
        err_box.setDisabled(False)
        if not path.exists(filename):
            # File does not exist
            err_box.setText("Invalid file!")
            err_box.show()
        elif self._hotkey.get_keys() is None or len(self._hotkey.get_keys()) == 0:
            # No keys
            err_box.setText(
                "Keys cant be empty!")
            err_box.show()
        elif self._hotkey_list.check_collision(self._hotkey):
            # Collision
            err_box.setText(
                "This hotkey colides with another one on this page!")
            err_box.show()
        elif filename.split(".")[-1] not in set(["ogg", "wav"]):
            # Invalid data type
            if check_if_program_present_in_path("ffmpeg"):
                # Try to use ffmpeg
                err_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                err_box.setText(
                    "Do you want to automatically convert this media into OGG using ffmpeg? (Create a copy in OGG format)")
                if err_box.exec() == QMessageBox.Ok:
                    # Convert the media into ogg (or at least try, let ffmpeg handle it)
                    ogg_filename = ".".join(filename.split(".")[0:-1]) + ".ogg"
                    info(f"Converting {filename} to {ogg_filename}")
                    ffmpeg_conversion(filename, ogg_filename)
                    self._hotkey.set_filename(ogg_filename)
                    self.accept()
            else:
                err_box.setText(
                    "This file format is not supported. Add FFMPEG to PATH to automatically convert")
        else:
            self.accept()
        self.setDisabled(False)

    def update_hotkey_display(self):
        text = " + ".join(self._hotkey.get_keys())
        text = text if not text == "" else "Awaiting input"
        self._ui.lKeys.setText(text)

    def update_file_display(self):
        text = self._hotkey.get_filename()
        self._ui.leFilePath.setText(text)

    def get_hotkey(self):
        return self._hotkey

    def scan_and_put_in_shortcut(self):
        scanned_keys = scan_pressed_keys()
        self._hotkey.set_keys(scanned_keys)
        self.on_hotkey_scan_complete()
