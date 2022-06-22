import json
from src.hotkey_reader import scan_pressed_keys
from ui.layouts.Ui_MainWindow import Ui_MainWindow
from PySide2.QtWidgets import (
    QMainWindow
)
from logging import info
from src.settings import Settings, CONFIG_FILENAME
from src.hotkey import Hotkey, HotkeyList, make_hotkey_from_dict
from ui.dialog_add_edit_file import AddEditFileDialog


class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        # UI setup
        super().__init__(parent)
        self._app = app
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._settings = Settings()
        self._hotkeys = HotkeyList()
        self._current_page = 0

        self.reload_config()

        # Set up triggers
        self._ui.tvHotkeys.itemDoubleClicked.connect(
            self.on_hotkey_dobule_clicked)
        self._ui.cbSource.textActivated.connect(self.on_add_hotkey)
        self._ui.bEdit.clicked.connect(self.on_edit_hotkey)
        self._ui.actionSave.triggered.connect(self.save_config)
        self._ui.actionReload.triggered.connect(self.reload_config)

    def on_hotkey_dobule_clicked(self, item):
        info(f"{item.text()} at {item.row()} {item.column()}")
        info(f"selection: {self._ui.tvHotkeys.selectedItems()[0].text()}")

    def on_add_hotkey(self, selected_type):
        info(f"Adding a new hotkey using {selected_type}")
        if selected_type == "Audio file":
            # Open dialog window
            dialog = AddEditFileDialog(self, self._hotkeys, self._current_page)
            dialog.show()

            if dialog.exec_():
                new_hotkey = dialog.get_hotkey()
                self._hotkeys.add_hotkey(new_hotkey)
                self.reload_table_contents()
                info(f"New hotkey added: {new_hotkey}")

    def on_edit_hotkey(self):
        keys = scan_pressed_keys()
        keys = " + ".join(keys)
        info(keys)
        pass

    def on_remove_hotkey(self):
        # TODO: implement this dialog
        pass

    def on_play(self):
        # TODO: implement this dialog
        pass

    def on_stop(self):
        # TODO: implement this dialog
        pass

    def on_prev_page(self):
        # TODO: implement this dialog
        pass

    def on_next_page(self):
        # TODO: implement this dialog
        pass

    def on_TTS_manager(self):
        # TODO: implement this dialog
        pass

    def reload_table_contents(self):
        pass

    def save_config(self):
        with open(CONFIG_FILENAME, "w") as config_file:
            data = {
                "settings": self._settings.save_to_dict(),
                "hotkeys": self._hotkeys.save_to_list()
            }
            json.dump(data, config_file)
        info("Settings and hotkeys saved!")

    def reload_config(self):
        try:
            with open(CONFIG_FILENAME, "r") as config_file:
                json_obj = json.load(config_file)
                self._settings.load_from_dict(json_obj["settings"])
                self._hotkeys.load_from_list(json_obj["hotkeys"])
            info("Settings and hotkeys reloaded!")
        except FileNotFoundError:
            info("Missing config file, using default settings")
