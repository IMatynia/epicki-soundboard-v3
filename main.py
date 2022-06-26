import logging as log
import sys
from PySide2.QtWidgets import QApplication
from ui.main_window import MainWindow
import os
from src.keyboard_hotkeys import HotkeyListener
from src.audio_handle import stop_all_sounds
from src.constants import DEFAULT_CUSTOM_FOLDER

log.basicConfig(
    format="[%(asctime)s->%(levelname)s->%(module)s" +
    "->%(funcName)s]: %(message)s",
    datefmt="%H:%M:%S",
    level=log.INFO
)


def setup():
    try:
        HotkeyListener.init()
        os.mkdir(DEFAULT_CUSTOM_FOLDER)
    except FileExistsError:
        # good
        pass


def closure():
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
