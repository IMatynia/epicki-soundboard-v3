import logging as log

log.basicConfig(
    filename="runtime.log",
    filemode="w",
    format="[%(asctime)s->%(levelname)s->%(module)s" +
    "->%(funcName)s]: %(message)s",
    datefmt="%H:%M:%S",
    level=log.INFO
)

from src.constants import DEFAULT_CUSTOM_FOLDER
from src.audio_handle import stop_all_sounds
from src.hotkey_listener import HotkeyListener
import os
from ui.main_window import MainWindow
from PySide2.QtWidgets import QApplication
import sys

def setup():
    HotkeyListener.init()
    if not os.path.exists(DEFAULT_CUSTOM_FOLDER):
        os.mkdir(DEFAULT_CUSTOM_FOLDER)


def closure():
    HotkeyListener.stop()
    stop_all_sounds()


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
