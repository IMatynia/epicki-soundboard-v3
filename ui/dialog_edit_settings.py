from src.audio_playback_provider import AudioPlaybackProvider
from src.config.config import AppConfig, Hotkey, KeyPress
from ui.layouts.Ui_SettingsDialog import Ui_SettingsDialog
from ui.utility_popup_box import MessageBoxesSimple
from ui.hotkey_scan_button import HotkeyScanPushButton
from PySide6.QtWidgets import QDialog, QLabel, QMainWindow, QGridLayout


class HotkeyScanUIElement:
    def __init__(
        self,
        parent,
        grid_layout: QGridLayout,
        row: int,
        label: str,
        attribute_name: str,
        default_keys: set[KeyPress],
    ) -> None:
        self._button = HotkeyScanPushButton(parent, default_keys)
        label_widget = QLabel(label, parent)
        grid_layout.addWidget(self._button, row, 1)
        grid_layout.addWidget(label_widget, row, 2)
        self._attribute_name = attribute_name

    def get_attribute_name(self) -> str:
        return self._attribute_name

    def get_hotkey(self) -> Hotkey | None:
        keys = self._button.get_keys()
        if keys:
            return Hotkey(keys=keys)
        else:
            return None


class EditSettingsDialog(QDialog):
    def __init__(self, parent, config: AppConfig) -> None:
        super().__init__(parent)
        self._ui = Ui_SettingsDialog()
        self._msg = MessageBoxesSimple(self)
        self._ui.setupUi(self)
        self._config = config

        # Set up hotkey buttons
        self._hk_scan_elements: list[HotkeyScanUIElement] = []
        self._set_up_hotkey_settings()

        # Connect buttons
        self._ui.bSave.clicked.connect(self.on_save)
        self._ui.bCancel.clicked.connect(self.on_cancel)

        # Fill in the combo box with devices
        for device in AudioPlaybackProvider.get_all_devices():
            self._ui.cbDeviceSelector.addItem(device.name, (device.name, device.index))

        current_selection = self._ui.cbDeviceSelector.findText(
            self._config.audio_config.additional_device_id or ""
        )
        self._ui.cbDeviceSelector.setCurrentIndex(current_selection)

        # Fill the form with remainig data
        self._ui.cPlayOnMain.setChecked(self._config.audio_config.main_device_on)
        self._ui.cPlaySingle.setChecked(
            self._config.audio_config.only_one_sound_at_once
        )

        self._ui.sbHorizontalWin.setValue(self._config.window_h_pos)
        self._ui.sbVerticalWin.setValue(self._config.window_v_pos)

        parent = self.parent()
        assert isinstance(parent, QMainWindow)
        horizontal, vertical = parent.pos().toTuple()  # type: ignore
        self._ui.lWindowPos.setText(f"{horizontal} x {vertical}")

    def _set_up_hotkey_settings(self):
        for row_it, (attribute_name, info_docs) in enumerate(
            self._config.app_hotkeys.get_all_hotkeys_as_attributes()
        ):
            self._hk_scan_elements.append(
                HotkeyScanUIElement(
                    self,
                    self._ui.glHotkeys,
                    row_it + 1,
                    info_docs or "N/A",
                    attribute_name,
                    getattr(self._config.app_hotkeys, attribute_name).keys,
                )
            )

    def on_save(self):
        # Apply device
        _, selected_device_id = self._ui.cbDeviceSelector.currentData()
        self._config.audio_config.additional_device_id = selected_device_id

        # Apply hotkeys
        for hotkey_element in self._hk_scan_elements:
            setattr(
                self._config.app_hotkeys,
                hotkey_element.get_attribute_name(),
                hotkey_element.get_hotkey(),
            )

        # Apply remaining data
        self._config.audio_config.main_device_on = self._ui.cPlayOnMain.isChecked()
        self._config.audio_config.only_one_sound_at_once = (
            self._ui.cPlaySingle.isChecked()
        )

        self._config.window_h_pos = self._ui.sbHorizontalWin.value()
        self._config.window_v_pos = self._ui.sbVerticalWin.value()

        self.accept()

    def on_cancel(self):
        self.reject()
