from ui.layouts.Ui_SettingsDialog import Ui_SettingsDialog
from ui.utility_popup_box import MessageBoxesInterface
from src.settings import Settings
from PySide2.QtWidgets import (
    QDialog
)
from src.audio_handle import get_devices_supporting_stereo_output


class EditSettingsDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent, settings: "Settings") -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._ui = Ui_SettingsDialog()
        self._ui.setupUi(self)
        self._settings = settings

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

    def on_save(self):
        selected_device_name, selected_device_id = self._ui.cbDeviceSelector.currentData()
        self._settings.set_additional_device(
            selected_device_name, selected_device_id)
        self.accept()

    def on_cancel(self):
        self.reject()
