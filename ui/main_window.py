import json
from src.hotkey_reader import scan_pressed_keys
from src.audio_handle import MultiAudioPlayThread, stop_all_sounds
from ui.layouts.Ui_MainWindow import Ui_MainWindow
from PySide2.QtWidgets import (
    QMainWindow, QTableWidgetItem
)
from logging import info
from src.settings import Settings, CONFIG_FILENAME
from src.hotkey import HotkeyList, Hotkey
from ui.dialog_add_edit_file import AddEditFileDialog


class HotkeyTableItemWidget(QTableWidgetItem):
    def __init__(self, text, hotkey_ref: "Hotkey") -> None:
        super().__init__()
        self._hotkey_ref = hotkey_ref
        self.setText(text)

    def get_hotkey_ref(self) -> "Hotkey":
        return self._hotkey_ref


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
        self._ui.bRemove.clicked.connect(self.on_remove_hotkey)
        self._ui.bPlay.clicked.connect(self.on_play)
        self._ui.bStop.clicked.connect(stop_all_sounds)
        self._ui.bNextPage.clicked.connect(self.on_next_page)
        self._ui.bPrevPage.clicked.connect(self.on_prev_page)

        self._ui.actionSave.triggered.connect(self.save_config)
        self._ui.actionReload.triggered.connect(self.reload_config)

        # Minor UI setup
        self._ui.lbPage.setText(f"{self._current_page}")

    def on_hotkey_dobule_clicked(self, item: "HotkeyTableItemWidget"):
        filename = item.get_hotkey_ref().get_filename()
        th = MultiAudioPlayThread(filename, self._settings)
        th.start()

    def on_add_hotkey(self, selected_type):
        if selected_type == "Audio file":
            # Open dialog window
            dialog = AddEditFileDialog(self, self._hotkeys, self._current_page)
            dialog.show()

            if dialog.exec_():
                new_hotkey = dialog.get_hotkey()
                self._hotkeys.add_hotkey(new_hotkey)
        elif selected_type == "Youtube-dl":
            pass
        elif selected_type == "Current TTS":
            pass
        self.reload_table_contents()

    def on_edit_hotkey(self):
        selected_item = self._ui.tvHotkeys.currentItem()
        if selected_item is None:
            return
        selection = selected_item.get_hotkey_ref()
        # Open dialog window
        dialog = AddEditFileDialog(
            self,
            self._hotkeys,
            self._current_page,
            selection.get_keys(),
            selection.get_filename())
        dialog.show()

        if dialog.exec_():
            new_hotkey = dialog.get_hotkey()
            self._hotkeys.remove_hotkey(selection)
            self._hotkeys.add_hotkey(new_hotkey)
            self.reload_table_contents()

    def on_remove_hotkey(self):
        hotkeys_to_remove = set()
        for selection in self._ui.tvHotkeys.selectedItems():
            hotkeys_to_remove.add(selection.get_hotkey_ref())

        for hotkey in hotkeys_to_remove:
            self._hotkeys.remove_hotkey(hotkey)
        self.reload_table_contents()

    def on_play(self):
        files_to_play = set()
        for selection in self._ui.tvHotkeys.selectedItems():
            files_to_play.add(selection.get_hotkey_ref().get_filename())

        for file in files_to_play:
            th = MultiAudioPlayThread(file, self._settings)
            th.start()

    def on_prev_page(self):
        if self._current_page > 0:
            self._current_page -= 1
            self._ui.lbPage.setText(f"{self._current_page}")
            self.reload_table_contents()

    def on_next_page(self):
        if self._current_page < self._hotkeys.get_max_pages()-1:
            self._current_page += 1
            self._ui.lbPage.setText(f"{self._current_page}")
            self.reload_table_contents()

    def on_TTS_manager(self):
        # TODO: implement this dialog
        pass

    def reload_table_contents(self):
        """Reloads all items in the table
        """
        hotkey_page = self._hotkeys.get_page(self._current_page)
        self._ui.tvHotkeys.setSortingEnabled(False)
        self._ui.tvHotkeys.clearContents()
        self._ui.tvHotkeys.setRowCount(len(hotkey_page))
        for i, hotkey in enumerate(hotkey_page):
            filename = hotkey.get_filename()
            keys_str = " + ".join(sorted(list(hotkey.get_keys())))
            # The keys
            item_keys = HotkeyTableItemWidget(keys_str, hotkey)
            self._ui.tvHotkeys.setItem(i, 0, item_keys)
            # The file
            item_file = HotkeyTableItemWidget(filename, hotkey)
            self._ui.tvHotkeys.setItem(i, 1, item_file)
        self._ui.tvHotkeys.setSortingEnabled(True)

    def save_config(self):
        """Saves current settings ang hotkeys into the config file
        """
        with open(CONFIG_FILENAME, "w") as config_file:
            data = {
                "settings": self._settings.save_to_dict(),
                "hotkeys": self._hotkeys.save_to_list()
            }
            json.dump(data, config_file, indent=4)
        info("Settings and hotkeys saved!")

    def reload_config(self):
        """Loads settings and hotkeys from the config file, reloads the table contents
        """
        try:
            with open(CONFIG_FILENAME, "r") as config_file:
                json_obj = json.load(config_file)
                self._settings.load_from_dict(json_obj["settings"])
                self._hotkeys.load_from_list(json_obj["hotkeys"])
            info("Settings and hotkeys reloaded!")
        except FileNotFoundError:
            info("Missing config file, using default settings")
        except json.JSONDecodeError:
            info("Config file invalid, using default settings")
        self.reload_table_contents()
