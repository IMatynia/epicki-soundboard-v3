from typing import Optional
from PySide6.QtCore import QTimer, QObject, Signal, QThread
from src.config.config import AppConfig
from ui.layouts.Ui_YoutubeDialog import Ui_AddYoutubeDL
from ui.utility_popup_box import MessageBoxesSimple
from ui.hotkey_scan_button import HotkeyScanPushButton
from PySide6.QtWidgets import QDialog
import threading
from enum import Enum, auto
import subprocess


class YoutubeDlDownloadWorker(QObject):
    log_signal = Signal(str)
    download_complete = Signal(type(Optional[str]))
    _process: subprocess.Popen
    _terminated: bool = False

    def terminate_download(self):
        self._terminated = True
        self._process.terminate()

    def download_media(self, media_url: str, name: str, config: AppConfig):
        binary = config.youtube_dl.bin_path
        extra_flags = config.youtube_dl.extra_arguments

        destination_path = (
            config.audio_config.get_download_cache_folder() / f"{name}.mp3"
        )

        try:
            self._process = subprocess.Popen(
                [
                    *extra_flags,
                    "-x",
                    "--audio-format",
                    config.audio_config.prefered_universal_format.value,
                    "--newline",
                    "--prefer-ffmpeg",
                    media_url,
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
            self.download_complete.emit(f"Cannot find downloader: {binary}")
            return
        except Exception as e:
            self.download_complete.emit(f"Error: {e}")
        
        assert self._process.stdout
        for line in self._process.stdout:
            self.log_signal.emit(line)

        if self._terminated:
            self.download_complete.emit("Terminated youtube-dl process!")
        elif self._process.poll():
            if not self._process.returncode == 0:
                self.download_complete.emit(
                    f"Youtube-dl zwrócił kod {self._process.returncode}"
                )
        else:
            self.download_complete.emit(None)


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
        self._thread = QThread(self)
        self._media_downloader = YoutubeDlDownloadWorker()
        self._media_downloader.moveToThread(self._thread)

        # State machine update loop
        self._state_mutex = threading.Semaphore()
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
        self._media_downloader.log_signal.connect(
            lambda log: self.update_state(download_log_message_changed=log)
        )
        self._media_downloader.download_complete.connect(
            lambda status: self.update_state(download_finished_with_error=status)
            if status
            else self.update_state(download_finished=True)
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
        with self._state_mutex:
            match self._state:
                case States.START:
                    self.set_status("Standby for download...")
                    self._ui.bActionButton.setEnabled(True)
                    self._ui.bActionButton.setText("Download")

                    if action_clicked:
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
                    self.set_status("Downloaded media!")
                    self._ui.bActionButton.setEnabled(True)
                    self._ui.bActionButton.setText("Save")

                    if url_changed:
                        self._state = States.START

                    if cancel_clicked:
                        self._state = States.STOP_reject

                    if action_clicked:
                        # Todo: Do the checks if all is good, save the hotkey to the config
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

    def begin_media_download(self):
        url = self._ui.leURL.text()
        name = self._ui.leName.text()
        config = self._config
        self._media_downloader.download_media(url, name, config)

    def cancel_media_download(self):
        self._media_downloader.terminate_download()

    def set_status(self, prompt):
        self._ui.lStatus.setText(prompt)
