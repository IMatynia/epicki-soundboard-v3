from PySide2.QtWidgets import QMessageBox


class MessageBoxesInterface:
    def __init__(self) -> None:
        self._info_box = QMessageBox(self)
        self._info_box.setWindowTitle("Soundboard - information")
        self._choice_box = QMessageBox(self)
        self._choice_box.setStandardButtons(
            QMessageBox.Ok | QMessageBox.Cancel)
        self._choice_box.setWindowTitle("Soundboard - choose your path")

    def show_popup(self, message):
        self._info_box.setDisabled(False)
        self._info_box.setText(message)
        return self._info_box.exec()

    def show_choice(self, message):
        self._choice_box.setDisabled(False)
        self._choice_box.setText(message)
        return self._choice_box.exec() == QMessageBox.Ok
