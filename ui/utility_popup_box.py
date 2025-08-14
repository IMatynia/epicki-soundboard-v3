from PySide6.QtWidgets import QMessageBox, QWidget


class MessageBoxesSimple:
    def __init__(self, parent_widget: QWidget) -> None:
        self._widget = parent_widget

    def show_popup(self, message, title: str = "Soundboard - info"):
        QMessageBox.information(self._widget, title, message)

    def show_choice(self, message: str, title: str = "Soundboard - choice"):
        message_box = QMessageBox(self._widget)
        message_box.setStandardButtons(
            message_box.StandardButton.Yes | message_box.StandardButton.No
        )
        message_box.setText(message)
        message_box.setWindowTitle(title)
        return message_box.exec() == QMessageBox.StandardButton.Yes

    def show_error(self, message, title: str = "Soundboard - ERROR!!!!!"):
        QMessageBox.critical(self._widget, title, message)
