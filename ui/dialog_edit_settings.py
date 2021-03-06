from ui.layouts.Ui_SettingsDialog import Ui_SettingsDialog
from ui.utility_popup_box import MessageBoxesInterface
from ui.hotkey_scan_button import HotkeyScanPushButton
from src.settings import Settings
from PySide2.QtWidgets import (
    QDialog, QLabel
)
from src.audio_devices import get_devices_supporting_stereo_output


class HotkeyScanUIElement:
    def __init__(self, parent, grid_layout, row, label, setter, getter) -> None:
        self._button = HotkeyScanPushButton(parent, getter())
        label = QLabel(label, parent)
        grid_layout.addWidget(self._button, row, 1)
        grid_layout.addWidget(label, row, 2)
        self._setter = setter

    def apply_hotkey(self):
        self._setter(self._button.get_keys())


class EditSettingsDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent, settings: "Settings") -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._ui = Ui_SettingsDialog()
        self._ui.setupUi(self)
        self._settings = settings

        # Set up hotkey buttons
        self._hk_scan_elements = []
        self._set_up_hotkey_buttons()

        # Connect buttons
        self._ui.bSave.clicked.connect(self.on_save)
        self._ui.bCancel.clicked.connect(self.on_cancel)

        # Fill in the combo box with devices
        devices = get_devices_supporting_stereo_output()
        for id in devices:
            self._ui.cbDeviceSelector.addItem(
                devices[id]["name"], (devices[id]["name"], id))

        current_selection = self._ui.cbDeviceSelector.findText(
            self._settings.get_additional_device())
        self._ui.cbDeviceSelector.setCurrentIndex(current_selection)

        # Fill the form with remainig data
        self._ui.cPlayOnMain.setChecked(self._settings.get_play_on_main())
        self._ui.cPlaySingle.setChecked(self._settings.get_is_singular())

        self._ui.sbHorizontalWin.setValue(self._settings.get_window_h_pos())
        self._ui.sbVerticalWin.setValue(self._settings.get_window_v_pos())

        horizontal, vertical = self.parent().pos().toTuple()
        self._ui.lWindowPos.setText(f"{horizontal} x {vertical}")

    def _set_up_hotkey_buttons(self):
        row = 1
        # Toggle main
        self._hk_scan_elements.append(HotkeyScanUIElement(
            self,
            self._ui.glHotkeys,
            row,
            "Toggles playback on default device",
            self._settings.set_keys_toggle_main,
            self._settings.get_keys_toggle_main
        ))
        row += 1

        # Toggle multiple
        self._hk_scan_elements.append(HotkeyScanUIElement(
            self,
            self._ui.glHotkeys,
            row,
            "Toggles playing singular file at once",
            self._settings.set_keys_toggle_singular,
            self._settings.get_keys_toggle_singular
        ))
        row += 1

        # Loud up
        self._hk_scan_elements.append(HotkeyScanUIElement(
            self,
            self._ui.glHotkeys,
            row,
            "Increases playback volume",
            self._settings.set_keys_loud_up,
            self._settings.get_keys_loud_up
        ))
        row += 1

        # Loud down
        self._hk_scan_elements.append(HotkeyScanUIElement(
            self,
            self._ui.glHotkeys,
            row,
            "Decrease playback volume",
            self._settings.set_keys_loud_down,
            self._settings.get_keys_loud_down
        ))
        row += 1

        # Silence
        self._hk_scan_elements.append(HotkeyScanUIElement(
            self,
            self._ui.glHotkeys,
            row,
            "Stop all sounds",
            self._settings.set_keys_silence,
            self._settings.get_keys_silence
        ))
        row += 1

        # Play TTS
        self._hk_scan_elements.append(HotkeyScanUIElement(
            self,
            self._ui.glHotkeys,
            row,
            "Play current TTS recording",
            self._settings.set_keys_tts_play,
            self._settings.get_keys_tts_play
        ))
        row += 1

        # Open TTS
        self._hk_scan_elements.append(HotkeyScanUIElement(
            self,
            self._ui.glHotkeys,
            row,
            "Open TTS manager",
            self._settings.set_keys_tts_open_manager,
            self._settings.get_keys_tts_open_manager
        ))
        row += 1

    def on_save(self):
        # Apply device
        selected_device_name, selected_device_id = self._ui.cbDeviceSelector.currentData()
        self._settings.set_additional_device(
            selected_device_name, selected_device_id)

        # Apply hotkeys
        for hotkey_element in self._hk_scan_elements:
            hotkey_element.apply_hotkey()
        self.accept()

        # Apply remaining data
        self._settings.set_play_on_main(self._ui.cPlayOnMain.isChecked())
        self._settings.set_singular_audio(self._ui.cPlaySingle.isChecked())

        self._settings.set_window_h_pos(self._ui.sbHorizontalWin.value())
        self._settings.set_window_v_pos(self._ui.sbVerticalWin.value())

    def on_cancel(self):
        self.reject()
