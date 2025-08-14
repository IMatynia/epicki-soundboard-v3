from src.config.config import AppConfig
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from src.translation_provider import TranslationProvider
from src.tts_provider import TTSProvider
from ui.utility_popup_box import MessageBoxesSimple
from ui.layouts.Ui_TTSManagerDialog import Ui_TTSManagerDialog
from logging import info


class TTSManagerDialog(QDialog):
    def __init__(self, parent, config: AppConfig) -> None:
        super().__init__(parent)
        self._msg = MessageBoxesSimple(self)

        self.setWindowFlags(self.windowFlags() ^ Qt.WindowType.WindowStaysOnTopHint)

        self._ui = Ui_TTSManagerDialog()
        self._ui.setupUi(self)
        self._config = config

        # Set up triggers
        self._ui.bCancel.clicked.connect(self.on_cancel)
        self._ui.bGenerate.clicked.connect(self.on_generate)
        self._ui.bTranslate.clicked.connect(self.on_translate)

        # Fill the language combo box
        self._ui.cbLanguage.addItems(TTSProvider.get_all_languages())
        self._ui.cbLanguage.setCurrentText(self._config.tts_config.language)

        # Fill in text box with the last prompt
        last_pompt = self._config.tts_config.prompt
        if last_pompt:
            self._ui.teText.setText(last_pompt)

    def on_cancel(self):
        self.reject()

    def on_generate(self):
        text = self._ui.teText.toPlainText()
        lang = self._ui.cbLanguage.currentText()

        self._config.tts_config.prompt = text
        self._config.tts_config.language = lang

        if len(text) == 0:
            self._msg.show_popup("Type in some text before generating!")
        else:
            try:
                TTSProvider.generate_tts(
                    text, lang, self._config.audio_config.get_tts_temporary_file_path()
                )
                self.accept()
            except Exception as e:
                info("TTS generation failed, details:")
                info(e)
                self._msg.show_popup(f"Could not generate: {e}, check log for more info")

    def on_translate(self):
        text = self._ui.teText.toPlainText()
        lang = self._ui.cbLanguage.currentText()
        if len(text) == 0:
            self._msg.show_popup("Type in some text before generating!")
        else:
            translated = TranslationProvider.translate(text, lang)
            self._ui.teText.setText(translated)
