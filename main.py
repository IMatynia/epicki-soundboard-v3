import logging as log
from src.audio_playback_provider import AudioPlaybackProvider
from src.hotkey_listener import HotkeyListener
from ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication
import sys


log.basicConfig(
    format="[%(asctime)s->%(levelname)s->%(module)s" + "->%(funcName)s]: %(message)s",
    datefmt="%H:%M:%S",
    level=log.INFO,
)


def setup():
    HotkeyListener.init()


def closure():
    HotkeyListener.stop()
    AudioPlaybackProvider.stop_all_sounds()


def main(args):
    setup()
    app = QApplication(args)
    window = MainWindow(app)
    window.show()
    ret_value = app.exec_()
    closure()
    return ret_value


if __name__ == "__main__":
    main(sys.argv)
