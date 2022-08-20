from PySide2.QtWidgets import QMessageBox, QAction


class MessageBoxesInterface:
    def __init__(self) -> None:
        pass

    def show_popup(self, message, title: str = "Soundboard - info"):
        QMessageBox.information(self, title, message)

    def show_choice(self, message: str, title: str = "Soundboard - choice"):
        message_box = QMessageBox(self)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setText(message)
        message_box.setWindowTitle(title)
        return message_box.exec() == QMessageBox.Yes

    def show_error(self, message, title: str = "Soundboard - ERROR!!!!!"):
        QMessageBox.critical(self, title, message)
