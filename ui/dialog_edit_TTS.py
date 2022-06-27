from logging import info
from ui.layouts.Ui_TTSManagerDialog import Ui_TTSManagerDialog
from ui.utility_popup_box import MessageBoxesInterface
from PySide2.QtWidgets import (
    QDialog
)
from src.gtts_handle import get_languages, generate_tts_ogg
from src.constants import TEMP_TTS_FILE


class TTSManagerDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent) -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._ui = Ui_TTSManagerDialog()
        self._ui.setupUi(self)

        # Set up triggers
        self._ui.bCancel.clicked.connect(self.on_cancel)
        self._ui.bGenerate.clicked.connect(self.on_generate)
        self._ui.bTranslate.clicked.connect(self.on_translate)

        # Fill the language combo box
        for language in get_languages():
            info(language)

    def on_cancel(self):
        self.reject()

    def on_generate(self):
        text = self._ui.teText.toPlainText()
        lang = self._ui.cbLanguage.currentData()

        if len(text) == 0:
            self.show_popup("Type in some text before generating!")
        else:
            generate_tts_ogg(text, lang, TEMP_TTS_FILE)
            self.accept()

    def on_translate(self):
        pass
