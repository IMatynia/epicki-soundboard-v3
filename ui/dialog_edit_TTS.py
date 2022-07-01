from src.constants import TEMP_TTS_FILE
from src.gtts_handle import get_languages, generate_tts_ogg
from src.settings import Settings
from PySide2.QtWidgets import (
    QDialog
)
from PySide2.QtCore import (
    Qt
)
from ui.utility_popup_box import MessageBoxesInterface
from ui.layouts.Ui_TTSManagerDialog import Ui_TTSManagerDialog
from logging import info
from gtts.tts import gTTSError


class TTSManagerDialog(QDialog, MessageBoxesInterface):
    def __init__(self, parent, settings: "Settings") -> None:
        QDialog.__init__(self, parent)
        MessageBoxesInterface.__init__(self)

        self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)

        self._ui = Ui_TTSManagerDialog()
        self._ui.setupUi(self)
        self._settings = settings

        # Set up triggers
        self._ui.bCancel.clicked.connect(self.on_cancel)
        self._ui.bGenerate.clicked.connect(self.on_generate)
        self._ui.bTranslate.clicked.connect(self.on_translate)

        # Fill the language combo box
        self._ui.cbLanguage.addItems(get_languages())
        self._ui.cbLanguage.setCurrentText(self._settings.get_tts_language())

        # Fill in text box with the last prompt
        last_pompt = self._settings.get_last_tts_prompt()
        if last_pompt:
            self._ui.teText.setText(last_pompt)

    def on_cancel(self):
        self.reject()

    def on_generate(self):
        text = self._ui.teText.toPlainText()
        lang = self._ui.cbLanguage.currentText()

        self._settings.set_last_tts_prompt(text)
        self._settings.set_tts_language(lang)

        if len(text) == 0:
            self.show_popup("Type in some text before generating!")
        else:
            try:
                generate_tts_ogg(text, lang, TEMP_TTS_FILE)
                self.accept()
            except gTTSError as e:
                info("GTTS generation failed, details:")
                info(e)
                self.show_popup("Could not generate, check log for more info")

    def on_translate(self):
        translator_works = True
        try:
            from translators import google
        except Exception as e:
            info("Google translator failed to initialize, details:")
            info(e)
            translator_works = False

        text = self._ui.teText.toPlainText()
        lang = self._ui.cbLanguage.currentText()
        if len(text) == 0:
            self.show_popup("Type in some text before generating!")
        elif not translator_works:
            self.show_popup(
                "Google translator is not working, check logs for more info")
        else:
            new_text = google(text, 'auto', lang)
            self._ui.teText.setText(new_text)
