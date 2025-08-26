from os import path
import os
from typing import Callable
import rtoml
from src.audio_playback_provider import AudioPlaybackProvider
from src.config import AppConfig
from src.config.config import AppSoundboardHotkey, Hotkey
from src.config.config import ConfigWrapper
from ui.hotkey_scan_button import keys_to_string
from ui.utility_popup_box import MessageBoxesSimple
from ui.layouts.Ui_MainWindow import Ui_MainWindow
from ui.dialog_add_edit_file import AddEditFileDialog
from ui.dialog_add_ytdl import AddYoutubeDialog
from ui.dialog_add_current_TTS import AddCurrentTTSDialog
from ui.dialog_edit_TTS import TTSManagerDialog
from ui.dialog_edit_settings import EditSettingsDialog
from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QInputDialog,
)
from PySide6.QtGui import QColor, QIcon
from logging import info
from src.hotkey_listener import HotkeyListener
from src.utils import get_shortened_filename
from src.config.constants import CONFIG_LOCATION

FILE_MISSING_COLOR = QColor(0xEE3311)


class HotkeyTableItemWidget(QTableWidgetItem):
    def __init__(self, text, hotkey_ref: AppSoundboardHotkey) -> None:
        super().__init__()
        self._hotkey_ref = hotkey_ref
        self.setText(text)

    def get_hotkey_ref(self) -> AppSoundboardHotkey:
        return self._hotkey_ref


class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        # UI setup
        super().__init__()
        self._msg = MessageBoxesSimple(self)
        self.setWindowIcon(QIcon("./media/logo.png"))

        self._app = app
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._config = ConfigWrapper()
        self._current_page = 1

        self.reload_config()

        self.set_up_triggers()

        # Minor UI setup
        self._ui.lbPage.setValue(self._current_page)
        self._ui.tvHotkeys.sortItems(0)
        with self._config.get() as config:
            self.move(config.window_h_pos, config.window_v_pos)

    def set_up_triggers(self):
        # Set up triggers
        self._ui.tvHotkeys.itemDoubleClicked.connect(self.on_hotkey_dobule_clicked)
        self._ui.cbSource.textActivated.connect(self.on_add_hotkey)

        self._ui.bEdit.clicked.connect(self.on_edit_hotkey)
        self._ui.bRemove.clicked.connect(self.on_remove_hotkey)
        self._ui.bPlay.clicked.connect(self.on_play)
        self._ui.bStop.clicked.connect(AudioPlaybackProvider.stop_all_sounds)
        self._ui.lbPage.textChanged.connect(self.on_page_change)

        # action triggers
        self._ui.actionEdit_settings.triggered.connect(self.on_edit_settings)
        self._ui.actionSave.triggered.connect(self.save_config)
        self._ui.actionReload.triggered.connect(self.reload_config)
        self._ui.actionOpen_tts_manager.triggered.connect(self.on_TTS_manager)
        self._ui.actionPlay_current_file.triggered.connect(self.play_temporary_tts)
        self._ui.action_Move_to_page.triggered.connect(self.on_move_to_page)
        self._ui.actionRemove_with_missing_files.triggered.connect(
            self.on_remove_hk_with_missing_files
        )
        self._ui.actionPurge_unused_files_in_customs_folder.triggered.connect(
            self.on_purge_unused
        )

    def on_hotkey_dobule_clicked(self, item: "HotkeyTableItemWidget"):
        filename = item.get_hotkey_ref().filename
        try:
            with self._config.get() as config:
                if config.audio_config.additional_device_id is None:
                    return
                AudioPlaybackProvider.play_audio_non_blocking_main_and_additional(
                    filename,
                    config.audio_config.additional_device_id,
                    config.audio_config.only_one_sound_at_once,
                    config.audio_config.main_device_on,
                )
        except FileNotFoundError:
            self._msg.show_error("File not found!")

    def on_add_hotkey(self, selected_type):
        with self._config.get() as config:
            if selected_type == "Audio file":
                # Open dialog window
                dialog = AddEditFileDialog(self, config, None, self._current_page)
                dialog.show()
                dialog.exec()
            elif selected_type == "Youtube-dl":
                dialog = AddYoutubeDialog(self, config, self._current_page)
                dialog.show()
                dialog.exec()
            elif selected_type == "Current TTS":
                if config.audio_config.get_tts_temporary_file_path().exists():
                    dialog = AddCurrentTTSDialog(
                        self,
                        config,
                        self._current_page,
                    )
                    dialog.show()
                    dialog.exec()
                else:
                    self._msg.show_popup(
                        "No temporary TTS file found. Generate one first."
                    )
        self.reload_table_contents()
        self.reload_hotkey_hooks()

    def on_edit_hotkey(self):
        selected_item = self._ui.tvHotkeys.currentItem()
        assert isinstance(selected_item, HotkeyTableItemWidget)

        if selected_item is None:
            return
        selection = selected_item.get_hotkey_ref()
        with self._config.get() as config:
            dialog = AddEditFileDialog(
                self,
                config,
                selection,
                self._current_page,
            )
            dialog.show()

        self.reload_table_contents()
        self.reload_hotkey_hooks()

    def on_remove_hotkey(self):
        with self._config.get() as config:
            hotkeys_to_remove: set[AppSoundboardHotkey] = self.get_selected_hotkeys()
            choice = self._msg.show_choice(
                f"Are you sure you want to remove {len(hotkeys_to_remove)} hotkeys?"
            )
            if not choice:
                return

            for hotkey in hotkeys_to_remove:
                config.remove_soundboard_hotkey(hotkey)

        self.reload_table_contents()
        self.reload_hotkey_hooks()

    def on_play(self):
        hotkeys_to_play = self.get_selected_hotkeys()
        files_to_play = set(map(lambda x: x.filename, hotkeys_to_play))

        with self._config.get() as config:
            for file in files_to_play:
                try:
                    if config.audio_config.additional_device_id is None:
                        return
                    AudioPlaybackProvider.play_audio_non_blocking_main_and_additional(
                        file,
                        config.audio_config.additional_device_id,
                        config.audio_config.only_one_sound_at_once,
                        config.audio_config.main_device_on,
                    )
                except FileNotFoundError:
                    # TODO: handle this excpetion
                    pass

    def play_temporary_tts(self):
        with self._config.get() as config:
            if config.audio_config.additional_device_id is None:
                return

            AudioPlaybackProvider.play_audio_non_blocking_main_and_additional(
                config.audio_config.get_tts_temporary_file_path(),
                config.audio_config.additional_device_id,
                config.audio_config.only_one_sound_at_once,
                config.audio_config.main_device_on,
            )

    def set_page_number(self, page_num: int):
        self._current_page = page_num
        self.reload_table_contents()
        self.reload_hotkey_hooks()

    def on_page_change(self):
        new_page_number = self._ui.lbPage.value()
        self.set_page_number(new_page_number)

    def on_prev_page(self):
        if self._current_page > 0:
            new_page_number = self._current_page - 1
            self._ui.lbPage.setValue(new_page_number)

    def on_next_page(self):
        new_page_number = self._current_page + 1
        self._ui.lbPage.setValue(new_page_number)

    def on_edit_settings(self):
        with self._config.get() as config:
            dialog = EditSettingsDialog(self, config)
            dialog.show()

        if dialog.exec_():
            self.reload_hotkey_hooks()

    def on_TTS_manager(self):
        with self._config.get() as config:
            dialog = TTSManagerDialog(self, config)
            dialog.show()
            dialog.exec_()

    def get_selected_hotkeys(self) -> set[AppSoundboardHotkey]:
        hotkeys: set[AppSoundboardHotkey] = set()
        for selection in self._ui.tvHotkeys.selectedItems():
            assert isinstance(selection, HotkeyTableItemWidget)
            hotkeys.add(selection.get_hotkey_ref())
        return hotkeys

    def on_move_to_page(self):
        new_page, accepted = QInputDialog.getInt(
            self,
            "Move selection",
            "Type in destination page number",
            self._current_page,
            0,
            1000,
            1,
        )
        if accepted:
            hotkeys_to_move = self.get_selected_hotkeys()

            info(f"Moving {len(hotkeys_to_move) // 2} hotkeys to page {new_page}")

            with self._config.get() as config:
                for hotkey in hotkeys_to_move:
                    config.remove_soundboard_hotkey(hotkey)
                    hotkey.page = new_page
                    config.add_soundboard_hotkey(hotkey)

            self.reload_table_contents()
            self.reload_hotkey_hooks()

    def on_remove_hk_with_missing_files(self):
        with self._config.get() as config:
            config: AppConfig
            current_page = config.get_soundboard_by_page(self._current_page)
            for hotkey in current_page:
                if not hotkey.filename.exists():
                    info(f"{hotkey} is missing it's file, removing")
                    config.remove_soundboard_hotkey(hotkey)

        self.reload_table_contents()
        self.reload_hotkey_hooks()

    def on_purge_unused(self):
        with self._config.get() as config:
            referenced_files = set(map(lambda x: x.filename, config.soundboard_hotkeys))

            for file in config.audio_config.get_download_cache_folder().iterdir():
                if file.is_file() and file not in referenced_files:
                    os.remove(file)
                    info(f"Removing {file}")

            for file in config.audio_config.get_tts_cache_folder().iterdir():
                if file.is_file() and file not in referenced_files:
                    os.remove(file)
                    info(f"Removing {file}")

    def closeEvent(self, event) -> None:
        if not self.check_config_changed():
            choice = self._msg.show_choice("Config changed, save it?")
            if choice:
                self.save_config()
        return super().closeEvent(event)

    def reload_table_contents(self):
        """Reloads all items in the table"""

        hotkey_page = []
        with self._config.get() as config:
            hotkey_page = config.get_soundboard_by_page(self._current_page)

        self._ui.tvHotkeys.setSortingEnabled(False)
        self._ui.tvHotkeys.clearContents()
        self._ui.tvHotkeys.setRowCount(len(hotkey_page))
        for i, sndbrd_hotkey in enumerate(hotkey_page):
            filename = sndbrd_hotkey.filename
            keys_str = keys_to_string(sndbrd_hotkey.hotkey.keys)
            # The keys
            item_keys = HotkeyTableItemWidget(keys_str, sndbrd_hotkey)
            # The file
            filename_short = get_shortened_filename(filename)
            item_file = HotkeyTableItemWidget(filename_short, sndbrd_hotkey)
            if not path.exists(filename):
                item_file.setBackground(FILE_MISSING_COLOR)
                item_keys.setBackground(FILE_MISSING_COLOR)

            self._ui.tvHotkeys.setItem(i, 0, item_keys)
            self._ui.tvHotkeys.setItem(i, 1, item_file)
        self._ui.tvHotkeys.setSortingEnabled(True)

    def reload_hotkey_hooks(self):
        # Hotkeys in the database
        info("Reloading all hotkeys")
        HotkeyListener.remove_all()
        with self._config.get() as config:
            for audio_hotkey in config.get_soundboard_by_page(self._current_page):

                def hotkey_callback():
                    with self._config.get() as config:
                        if config.audio_config.additional_device_id is None:
                            return
                        AudioPlaybackProvider.play_audio_non_blocking_main_and_additional(
                            audio_hotkey.filename,
                            config.audio_config.additional_device_id,
                            config.audio_config.only_one_sound_at_once,
                            config.audio_config.main_device_on,
                        )

                HotkeyListener.add_hotkey(
                    audio_hotkey.hotkey.keys,
                    hotkey_callback,
                )

        # QOL shortkeys
        with self._config.get() as config:
            qol: list[tuple[Hotkey, Callable]] = [
                (
                    config.app_hotkeys.stop_all_sounds,
                    AudioPlaybackProvider.stop_all_sounds,
                ),
                (
                    config.app_hotkeys.toggle_main_device_playback,
                    self._config.toggle_play_on_main,
                ),
                (
                    config.app_hotkeys.toggle_singular_playback,
                    self._config.toggle_singular_playback,
                ),
                (config.app_hotkeys.play_cached_tts, self.play_temporary_tts),
                (
                    config.app_hotkeys.open_tts_manager,
                    self._ui.actionOpen_tts_manager.trigger,
                ),
                (
                    config.app_hotkeys.increase_volume,
                    lambda: self._config.increase_volume,
                ),
                (
                    config.app_hotkeys.decrease_volume,
                    lambda: self._config.decrease_volume,
                ),
                (config.app_hotkeys.next_page, self.on_next_page),
                (config.app_hotkeys.previous_page, self.on_prev_page),
            ]

        for hotkey, callback in qol:
            HotkeyListener.add_hotkey(hotkey.keys, callback)

    def check_config_changed(self):
        if not CONFIG_LOCATION.exists():
            return True
        config_in_file_dict = rtoml.load(CONFIG_LOCATION)
        with self._config.get() as config_in_memory:
            return not config_in_file_dict == config_in_memory.model_dump(mode="json")

    def save_config(self):
        """Saves current settings ang hotkeys into the config file"""
        with self._config.get() as config:
            rtoml.dump(config.model_dump(mode="json"), CONFIG_LOCATION, pretty=True)
        info("Settings and hotkeys saved!")

    def reload_config(self):
        """Loads settings and hotkeys from the config file, reloads the table contents"""
        if CONFIG_LOCATION.exists():
            config_dict = rtoml.load(CONFIG_LOCATION)
            self._config.set(AppConfig.model_validate(config_dict))
        else:
            self._config.set(AppConfig())

        self.reload_table_contents()
        self.reload_hotkey_hooks()
