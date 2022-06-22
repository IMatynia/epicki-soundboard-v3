import logging as log
import sys
from PySide2.QtWidgets import QApplication
from ui.main_window import MainWindow

log.basicConfig(
    format="[%(asctime)s->%(levelname)s->%(module)s" +
    "->%(funcName)s]: %(message)s",
    datefmt="%H:%M:%S",
    level=log.INFO
)


def main(args):
    app = QApplication(args)
    window = MainWindow(app)
    window.show()
    return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
