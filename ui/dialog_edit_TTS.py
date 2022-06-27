from logging import info
from translators import google
from ui.layouts.Ui_TTSManagerDialog import Ui_TTSManagerDialog
from ui.utility_popup_box import MessageBoxesInterface
from PySide2.QtWidgets import (
    QDialog
)
from src.gtts_handle import get_languages, generate_tts_ogg
from src.constants import TEMP_TTS_FILE


class TTSManagerDialog(QDialog, MessageBoxesInterface):
    _DEFAULT_LANGUAGE = "en"

    def __init__(self, parent, settings) -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)
        self._ui = Ui_TTSManagerDialog()
        self._ui.setupUi(self)
        self._settings = settings

        # Set up triggers
        self._ui.bCancel.clicked.connect(self.on_cancel)
        self._ui.bGenerate.clicked.connect(self.on_generate)
        self._ui.bTranslate.clicked.connect(self.on_translate)

        # Fill the language combo box
        self._ui.cbLanguage.addItems(get_languages())
        self._ui.cbLanguage.setCurrentText(TTSManagerDialog._DEFAULT_LANGUAGE)

    def on_cancel(self):
        self.reject()

    def on_generate(self):
        text = self._ui.teText.toPlainText()
        lang = self._ui.cbLanguage.currentText()

        if len(text) == 0:
            self.show_popup("Type in some text before generating!")
        else:
            generate_tts_ogg(text, lang, TEMP_TTS_FILE)
            self.accept()

    def on_translate(self):
        text = self._ui.teText.toPlainText()
        lang = self._ui.cbLanguage.currentText()
        if len(text) == 0:
            self.show_popup("Type in some text before generating!")
        else:
            new_text = google(text, 'auto', lang)
            self._ui.teText.setText(new_text)
