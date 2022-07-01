import json
from os import path
from src.audio_handle import multi_audio_play_async, stop_all_sounds
from ui.utility_popup_box import MessageBoxesInterface
from ui.layouts.Ui_MainWindow import Ui_MainWindow
from ui.dialog_add_edit_file import AddEditFileDialog
from ui.dialog_add_ytdl import AddYoutubeDialog
from ui.dialog_add_current_TTS import AddCurrentTTSDialog
from ui.dialog_edit_TTS import TTSManagerDialog
from ui.dialog_edit_settings import EditSettingsDialog
from PySide2.QtWidgets import (
    QMainWindow, QTableWidgetItem, QInputDialog
)
from PySide2.QtGui import (
    QColor
)
from logging import info
from src.settings import Settings
from src.constants import TEMP_TTS_FILE, CONFIG_FILENAME, DEFAULT_SOUND_MULTIPLIER
from src.audio_hotkey import AudioHotkeyList, AudioHotkey
from src.key import keys_to_string, Key
from src.hotkey_listener import HotkeyListener
from src.utils import check_if_program_present_in_path, get_shortened_filename


class HotkeyTableItemWidget(QTableWidgetItem):
    def __init__(self, text, hotkey_ref: "AudioHotkey") -> None:
        super().__init__()
        self._hotkey_ref = hotkey_ref
        self.setText(text)

    def get_hotkey_ref(self) -> "AudioHotkey":
        return self._hotkey_ref


class MainWindow(QMainWindow, MessageBoxesInterface):
    def __init__(self, app, parent=None):
        # UI setup
        QMainWindow.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._app = app
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._settings = Settings()
        self._hotkeys = AudioHotkeyList()
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

        # action triggers
        self._ui.actionEdit_settings.triggered.connect(self.on_edit_settings)
        self._ui.actionSave.triggered.connect(self.save_config)
        self._ui.actionReload.triggered.connect(self.reload_config)
        self._ui.actionOpen_tts_manager.triggered.connect(self.on_TTS_manager)
        self._ui.actionPlay_current_file.triggered.connect(
            self.play_temporary_tts)
        self._ui.action_Move_to_page.triggered.connect(self.on_move_to_page)
        # self._ui.actionRemove_with_missing_files.connect(
        #     self.on_remove_missing_files)

        # Minor UI setup
        self._ui.lbPage.setText(f"{self._current_page}")
        self._ui.tvHotkeys.sortItems(0)
        self.move(self._settings.get_window_h_pos(),
                  self._settings.get_window_v_pos())

    def on_hotkey_dobule_clicked(self, item: "HotkeyTableItemWidget"):
        filename = item.get_hotkey_ref().get_filename()
        try:
            multi_audio_play_async(filename, self._settings)
        except FileNotFoundError:
            # TODO: handle this excpetion
            pass

    def on_add_hotkey(self, selected_type):
        if selected_type == "Audio file":
            # Open dialog window
            dialog = AddEditFileDialog(self, self._hotkeys, self._current_page)
            dialog.show()

            if dialog.exec_():
                new_hotkey = dialog.get_hotkey()
                self._hotkeys.add_hotkey(new_hotkey)
        elif selected_type == "Youtube-dl":
            if check_if_program_present_in_path("ffmpeg") and check_if_program_present_in_path("youtube-dl"):
                dialog = AddYoutubeDialog(
                    self, self._hotkeys, self._current_page)
                dialog.show()

                if dialog.exec_():
                    new_hotkey = dialog.get_hotkey()
                    self._hotkeys.add_hotkey(new_hotkey)
            else:
                self.show_popup(
                    "You need ffmpeg and youtube-dl in path to use this feature!")
        elif selected_type == "Current TTS":
            if path.exists(TEMP_TTS_FILE):
                dialog = AddCurrentTTSDialog(
                    self, 
                    self._hotkeys,
                    self._settings.get_tts_language(),
                    self._settings.get_last_tts_prompt(), 
                    self._current_page)
                dialog.show()

                if dialog.exec_():
                    new_hotkey = dialog.get_hotkey()
                    self._hotkeys.add_hotkey(new_hotkey)
            else:
                self.show_popup(
                    "No temporary TTS file found. Did you forget to generate it?")
        self.reload_table_contents()
        self.reload_hotkey_hooks()

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
            self.reload_hotkey_hooks()

    def on_remove_hotkey(self):
        hotkeys_to_remove = set()
        for selection in self._ui.tvHotkeys.selectedItems():
            hotkeys_to_remove.add(selection.get_hotkey_ref())

        choice = self.show_choice(
            f"Are you sure you want to remove {len(hotkeys_to_remove)} hotkeys?")
        if not choice:
            return

        for hotkey in hotkeys_to_remove:
            self._hotkeys.remove_hotkey(hotkey)
        self.reload_table_contents()
        self.reload_hotkey_hooks()

    def on_play(self):
        files_to_play = set()
        for selection in self._ui.tvHotkeys.selectedItems():
            files_to_play.add(selection.get_hotkey_ref().get_filename())

        for file in files_to_play:
            try:
                multi_audio_play_async(file, self._settings)
            except FileNotFoundError:
                # TODO: handle this excpetion
                pass

    def play_temporary_tts(self):
        multi_audio_play_async(TEMP_TTS_FILE, self._settings)

    def on_prev_page(self):
        if self._current_page > 0:
            self._current_page -= 1
            self._ui.lbPage.setText(f"{self._current_page}")
            self.reload_table_contents()
            self.reload_hotkey_hooks()

    def on_next_page(self):
        if self._current_page < self._hotkeys.get_max_pages()-1:
            self._current_page += 1
            self._ui.lbPage.setText(f"{self._current_page}")
            self.reload_table_contents()
            self.reload_hotkey_hooks()

    def on_edit_settings(self):
        dialog = EditSettingsDialog(self, self._settings)
        dialog.show()

        if dialog.exec_():
            self.reload_hotkey_hooks()

    def on_TTS_manager(self):
        dialog = TTSManagerDialog(self, self._settings)
        dialog.show()
        dialog.exec_()

    def on_move_to_page(self):
        new_page, accepted = QInputDialog.getInt(self,
                                                 "Move selection",
                                                 "Type in destination page number",
                                                 self._current_page,
                                                 0,
                                                 self._hotkeys.get_max_pages(),
                                                 1)
        if accepted:
            hotkeys_to_move = set()
            for selection in self._ui.tvHotkeys.selectedItems():
                hotkeys_to_move.add(selection.get_hotkey_ref())

            info(
                f"Moving {len(hotkeys_to_move)//2} hotkeys to page {new_page}")

            for hotkey in hotkeys_to_move:
                self._hotkeys.remove_hotkey(hotkey)
                hotkey.set_page(new_page)
                self._hotkeys.add_hotkey(hotkey)

            self.reload_table_contents()
            self.reload_hotkey_hooks()

    def closeEvent(self, event) -> None:
        if not self.check_config_changed():
            choice = self.show_choice("Config changed, save it?")
            if choice:
                self.save_config()
        return super().closeEvent(event)

    def reload_table_contents(self):
        """Reloads all items in the table
        """
        FILE_MISSING_COLOR = QColor(0xEE3311)

        hotkey_page = self._hotkeys.get_page(self._current_page)
        self._ui.tvHotkeys.setSortingEnabled(False)
        self._ui.tvHotkeys.clearContents()
        self._ui.tvHotkeys.setRowCount(len(hotkey_page))
        for i, hotkey in enumerate(hotkey_page):
            filename = hotkey.get_filename()
            keys_str = keys_to_string(hotkey.get_keys())
            # The keys
            item_keys = HotkeyTableItemWidget(keys_str, hotkey)
            # The file
            filename_short = get_shortened_filename(filename)
            item_file = HotkeyTableItemWidget(filename_short, hotkey)
            if not path.exists(filename):
                item_file.setBackgroundColor(FILE_MISSING_COLOR)
                item_keys.setBackgroundColor(FILE_MISSING_COLOR)

            self._ui.tvHotkeys.setItem(i, 0, item_keys)
            self._ui.tvHotkeys.setItem(i, 1, item_file)
        self._ui.tvHotkeys.setSortingEnabled(True)

    def reload_hotkey_hooks(self):
        # Hotkeys in the database
        info("Reloading all hotkeys")
        HotkeyListener.remove_all()
        for audio_hotkey in self._hotkeys.get_page(self._current_page):
            HotkeyListener.add_hotkey(audio_hotkey.get_keys(),
                                      multi_audio_play_async,
                                      [audio_hotkey.get_filename(), self._settings])

        # QOL shortkeys

        # Stop sounds
        HotkeyListener.add_hotkey(
            self._settings.get_keys_silence(),
            stop_all_sounds
        )

        # Toggle play on main
        HotkeyListener.add_hotkey(
            self._settings.get_keys_toggle_main(),
            self._settings.toggle_play_on_main
        )

        # Toggle singular
        HotkeyListener.add_hotkey(
            self._settings.get_keys_toggle_singular(),
            self._settings.toggle_singular_audio
        )

        # Play tts
        HotkeyListener.add_hotkey(
            self._settings.get_keys_tts_play(),
            self.play_temporary_tts
        )

        # Open tts manager TODO: make this use signals so that it works
        # HotkeyListener.add_hotkey(
        #     self._settings.get_keys_tts_open_manager(),
        #     self.on_TTS_manager
        # )

        # Increase volume
        HotkeyListener.add_hotkey(
            self._settings.get_keys_loud_up(),
            self._settings.modify_volume_multiplier,
            [DEFAULT_SOUND_MULTIPLIER]
        )

        # Decrease volume
        HotkeyListener.add_hotkey(
            self._settings.get_keys_loud_down(),
            self._settings.modify_volume_multiplier,
            [1/DEFAULT_SOUND_MULTIPLIER]
        )

        # Next page
        HotkeyListener.add_hotkey(
            {Key(">", 39)},
            self._ui.bNextPage.click
        )

        # Prev page
        HotkeyListener.add_hotkey(
            {Key("<", 37)},
            self._ui.bPrevPage.click
        )

    def check_config_changed(self):
        current_data = {
            "settings": self._settings.save_to_dict(),
            "hotkeys": self._hotkeys.save_to_list()
        }

        data_in_file = None
        try:
            with open(CONFIG_FILENAME, "r") as config_file:
                data_in_file = json.load(config_file)
        except FileNotFoundError:
            info("Missing config file")
        except json.JSONDecodeError:
            info("Config file invalid")

        return current_data == data_in_file

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
        self.reload_hotkey_hooks()
