import logging
from pathlib import Path
from PySide6.QtCore import (
    Qt,
    QTimer,
    QObject,
    Signal,
    Slot,
    QRunnable,
    QThreadPool,
    QSemaphore,
)
from src.config.config import AppConfig, AppSoundboardHotkey, Hotkey
from ui.layouts.Ui_YoutubeDialog import Ui_AddYoutubeDL
from ui.utility_popup_box import MessageBoxesSimple
from ui.hotkey_scan_button import HotkeyScanPushButton
from PySide6.QtWidgets import QDialog
import threading
from enum import Enum, auto
import subprocess
import signal
import os


class DownloaderSignals(QObject):
    download_complete = Signal()
    """Sent upon completion, means it succeeded"""
    download_error = Signal(str)
    """Contains the error message"""
    log_signal = Signal(str)
    """Logs sent during download process"""


class YoutubeDlDownloadWorker(QRunnable):
    signals: DownloaderSignals
    _process: subprocess.Popen | None = None
    _terminated: bool = False
    _media_url: str
    _path: Path
    _config: AppConfig

    def __init__(self, media_url: str, path: Path, config: AppConfig) -> None:
        super().__init__()
        self._media_url = media_url
        self._path = path
        self._config = config
        self.signals = DownloaderSignals()

    @Slot()
    def terminate_download(self):
        self._terminated = True
        logging.warning("Terminating download process")
        if self._process and self._process.poll() is None:
            try:
                # WINDOWS ODDITY
                os.kill(self._process.pid, signal.CTRL_C_EVENT)
            except Exception as e:
                self.signals.download_error.emit(f"Failed to terminate: {e}")

    @Slot()
    def run(self):
        binary = self._config.youtube_dl.bin_path
        extra_flags = self._config.youtube_dl.extra_arguments

        destination_path = self._path

        try:
            self._process = subprocess.Popen(
                [
                    *extra_flags,
                    "-x",
                    "--audio-format",
                    self._config.audio_config.prefered_universal_format.value,
                    "--newline",
                    "--prefer-ffmpeg",
                    self._media_url,
                    "-o",
                    destination_path,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                executable=binary,
                universal_newlines=True,
                encoding="utf-8",
                bufsize=1,
                text=True,
            )
        except FileNotFoundError:
            self.signals.download_error.emit(f"Cannot find downloader: {binary}")
            return
        except Exception as e:
            self.signals.download_error.emit(f"Error: {e}")
            return

        # Thread to read stdout in real time
        def read_stdout():
            assert self._process and self._process.stdout is not None
            for line in self._process.stdout:
                self.signals.log_signal.emit(line.rstrip())

        # Thread to read stderr in real time
        def read_stderr():
            assert self._process and self._process.stderr is not None
            for line in self._process.stderr:
                self.signals.log_signal.emit(line.rstrip())

        stdout_thread = threading.Thread(target=read_stdout)
        stderr_thread = threading.Thread(target=read_stderr)

        stdout_thread.start()
        stderr_thread.start()

        # Wait for process to finish
        return_code = self._process.wait()

        # Join threads to ensure all output is processed
        stdout_thread.join()
        stderr_thread.join()

        if self._terminated:
            self.signals.download_error.emit("Terminated youtube-dl process!")
            return

        if return_code == 0:
            self.signals.download_complete.emit()
        else:
            self.signals.download_error.emit(
                f"Youtube-dl exited with code {self._process.returncode}, consult the logs"
            )


class States(Enum):
    START = auto()
    DownloadingMedia = auto()
    CancellingMediaDownload = auto()
    MediaDownloadedInCache = auto()
    FinalChecksBeforeSaving = auto()
    STOP_reject = auto()
    STOP_accept = auto()


class AddYoutubeDialog(QDialog):
    def __init__(self, parent, config: AppConfig, page: int) -> None:
        super().__init__(parent)
        self._msg = MessageBoxesSimple(self)
        self._ui = Ui_AddYoutubeDL()
        self._ui.setupUi(self)
        self._page = page
        self._config = config
        self._thread_pool = QThreadPool(self)
        self._current_media_downloader: YoutubeDlDownloadWorker | None = None
        self._cached_file_location: Path | None = None

        # State machine update loop
        self._state_mutex = QSemaphore(1)
        self._state: States = States.START
        self._state_machine_timer = QTimer(self, interval=100)
        self._state_machine_timer.timeout.connect(
            lambda: self.update_state(idle_update=True)
        )
        self._state_machine_timer.start()

        # Set up triggers
        self._scan_button = HotkeyScanPushButton(self)
        self._ui.buttonPlaceholder.addWidget(self._scan_button)

        self._ui.bActionButton.clicked.connect(
            lambda: self.update_state(action_clicked=True)
        )
        self._ui.bCancel.clicked.connect(lambda: self.update_state(cancel_clicked=True))
        self._ui.leURL.textChanged.connect(
            lambda url: self.update_state(url_changed=url)
        )

        self.update_state(idle_update=True)

    def update_state(
        self,
        action_clicked=False,
        download_finished=False,
        download_finished_with_error: str | None = None,
        url_changed: str | None = None,
        download_log_message_changed: str | None = None,
        cancel_clicked=False,
        idle_update=False,
    ):
        # Update state
        self._state_machine_timer.stop()
        self._state_mutex.acquire()
        if not idle_update:
            logging.debug(f"State before: {self._state}")
        match self._state:
            case States.START:
                self.set_status("Standby for download...")
                self._ui.bActionButton.setEnabled(True)
                self._ui.bActionButton.setText("Download")

                if action_clicked and self._current_media_downloader is None:
                    self.begin_media_download()
                    self._state = States.DownloadingMedia

                if cancel_clicked:
                    self.setEnabled(False)
                    self._state = States.STOP_reject

            case States.DownloadingMedia:
                self._ui.bActionButton.setEnabled(False)
                self._ui.bActionButton.setText("Downloading...")

                if download_log_message_changed:
                    self.set_status(download_log_message_changed)

                if download_finished:
                    self._state = States.MediaDownloadedInCache

                if download_finished_with_error:
                    self._msg.show_error(
                        f"Error during download: {download_finished_with_error}"
                    )
                    self._state = States.START

                if cancel_clicked:
                    self.cancel_media_download()
                    self._state = States.CancellingMediaDownload

            case States.MediaDownloadedInCache:
                self._current_media_downloader = None
                self.set_status("Downloaded media!")
                self._ui.bActionButton.setEnabled(True)
                self._ui.bActionButton.setText("Save")

                if url_changed:
                    self._state = States.START

                if cancel_clicked:
                    self._state = States.STOP_reject

                if action_clicked:
                    res = self.validate_inputs()
                    if res:
                        self._config.add_soundboard_hotkey(res)
                        self._state = States.STOP_accept

            case States.CancellingMediaDownload:
                self._ui.bActionButton.setEnabled(False)
                self.set_status("Cancelling download...")

                if download_finished_with_error or download_finished:
                    self._state = States.START

            case States.STOP_reject:
                self.reject()

            case States.STOP_accept:
                self.accept()

        if not idle_update:
            logging.debug(f"State after: {self._state}")
        self._state_mutex.release()
        self._state_machine_timer.start()

    def begin_media_download(self):
        url = self._ui.leURL.text()
        name = self._ui.leName.text()
        config = self._config

        self._cached_file_location = (
            config.audio_config.get_download_cache_file_by_name(name)
        )

        media_downloader = YoutubeDlDownloadWorker(
            url, self._cached_file_location, config
        )

        media_downloader.signals.log_signal.connect(
            self.update_log, type=Qt.ConnectionType.QueuedConnection
        )
        media_downloader.signals.download_complete.connect(
            self.update_notify_download_finished,
            type=Qt.ConnectionType.QueuedConnection,
        )
        media_downloader.signals.download_error.connect(
            self.update_notify_download_failed, type=Qt.ConnectionType.QueuedConnection
        )
        media_downloader.signals.log_signal.connect(logging.info)
        media_downloader.signals.download_error.connect(logging.error)

        assert self._current_media_downloader is None
        self._current_media_downloader = media_downloader
        self._thread_pool.start(self._current_media_downloader)

    def validate_inputs(self) -> AppSoundboardHotkey | None:
        hotkey = self._scan_button.get_keys()
        if not hotkey:
            self._msg.show_error("No hotkey set!")
            return None
        if not self._cached_file_location or not self._cached_file_location.exists():
            self._msg.show_error("No file in cache!")
            return None
        return AppSoundboardHotkey(
            page=self._page,
            hotkey=Hotkey(keys=hotkey),
            filename=self._cached_file_location,
        )

    @Slot(str)
    def update_log(self, new_log: str):
        self.update_state(download_log_message_changed=new_log)

    @Slot()
    def update_notify_download_finished(self):
        self.update_state(download_finished=True)

    @Slot(str)
    def update_notify_download_failed(self, message: str):
        self.update_state(download_finished_with_error=message)

    def cancel_media_download(self):
        self._cached_file_location = None
        if self._current_media_downloader:
            self._current_media_downloader.terminate_download()

    def set_status(self, prompt):
        self._ui.lStatus.setText(prompt)
