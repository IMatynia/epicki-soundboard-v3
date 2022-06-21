from ui.layouts.Ui_MainWindow import Ui_MainWindow
from PySide2.QtWidgets import (
    QMainWindow
)
from logging import info


class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        # UI setup
        super().__init__(parent)
        self._app = app
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.reload_settings()

        # Set up triggers
        self._ui.tvHotkeys.itemDoubleClicked.connect(self.hotkeyDoubleClicked)
        self._ui.bEdit.clicked.connect(self.onEditHotkey)
        self._ui.bEdit.clicked.connect(self.onEditHotkey)
        self._ui.bEdit.clicked.connect(self.onEditHotkey)
        self._ui.bEdit.clicked.connect(self.onEditHotkey)

    def hotkeyDoubleClicked(self, item):
        info(f"{item.text()} at {item.row()} {item.column()}")
        info(f"selection: {self._ui.tvHotkeys.selectedItems()[0].text()}")

    def onAddHotkey(self):
        # TODO: implement this dialog
        pass

    def onEditHotkey(self):
        # TODO: implement this dialog
        pass

    def onRemoveHotkey(self):
        # TODO: implement this dialog
        pass

    def onPlay(self):
        # TODO: implement this dialog
        pass

    def onStop(self):
        # TODO: implement this dialog
        pass

    def onPrevPage(self):
        # TODO: implement this dialog
        pass

    def onNextPage(self):
        # TODO: implement this dialog
        pass

    def onTTSManager(self):
        # TODO: implement this dialog
        pass

    def saveSettings(self):
        pass

    def reloadSettings(self):
        # implement settings reload TODO:
        pass
