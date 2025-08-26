from copy import copy
from pathlib import Path
from src.config.config import (
    AppConfig,
    AppSoundboardHotkey,
    Hotkey,
    SupportedPlaybackFormats,
)
from ui.layouts.Ui_AddEditFileDialog import Ui_AddEditFileDialog
from ui.hotkey_scan_button import HotkeyScanPushButton
from ui.utility_popup_box import MessageBoxesSimple
from PySide6.QtWidgets import QDialog, QFileDialog
from logging import info


class AddEditFileDialog(QDialog):
    _og: AppSoundboardHotkey | None

    def __init__(
        self,
        parent,
        config: AppConfig,
        edited_hotkey: AppSoundboardHotkey | None,
        current_page: int,
    ) -> None:
        super().__init__(parent)
        self._msg = MessageBoxesSimple(self)
        self._config = config
        self._ui = Ui_AddEditFileDialog()
        self._ui.setupUi(self)
        if edited_hotkey:
            self._og = copy(edited_hotkey)
            self.update_file_display(edited_hotkey.filename)
            keys = edited_hotkey.hotkey.keys
        else:
            self._og = None
            keys = None
        self._page = current_page
        self._soundboard_hotkey = None

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
            return

        self.update_file_display(Path(file))

    def on_save(self):
        filename = Path(self._ui.leFilePath.text())
        keys = self._scan_button.get_keys()

        if filename is None or keys is None:
            self._msg.show_popup("Missing filename or keys!")
            return

        if not filename.exists():
            self._msg.show_popup("File does not exist!")
            return

        hotkey = Hotkey(keys=keys)
        if self._config.check_for_collisions(hotkey, self._page):
            self._msg.show_popup("The hotkey is colliding with a different one!")
            return

        if filename.suffix[1:] not in SupportedPlaybackFormats:
            choice = self._msg.show_choice(
                f"Unsupported media format chosen, would you like to convert it to prefered format? ({self._config.audio_config.prefered_universal_format})"
            )
            if choice:
                # TODO: Handle conversion using the new dependency
                self._msg.show_popup("TODO Format conversion")
                return
            else:
                return

        self._soundboard_hotkey = AppSoundboardHotkey(
            page=self._page, hotkey=hotkey, filename=filename
        )
        self.accept()

    def accept(self) -> None:
        if self._soundboard_hotkey:
            if self._og:
                self._config.remove_soundboard_hotkey(self._og)
            self._config.add_soundboard_hotkey(self._soundboard_hotkey)
        return super().accept()

    def update_file_display(self, filename: Path):
        self._ui.leFilePath.setText(str(filename))
