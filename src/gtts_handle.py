from os import remove
from src.ffmpeg_handle import ffmpeg_conversion
import gtts

_LANGUAGE_LIST = list(gtts.lang.tts_langs())
TEMP_TTS_FILE = "temp.mp3"


class InvalidLanguageError(Exception):
    pass


def get_languages():
    return _LANGUAGE_LIST


def generate_tts_ogg(text, lang, filename):
    """Creates a google TTS file of a given filename

    Args:
        text (str): the text to speak
        lang (str): language code (only the ones accepted by gtts are allowed)
        filename (str): destination file (extension must be provided)
    """
    if lang not in get_languages():
        raise InvalidLanguageError()

    tts = gtts.gTTS(text=text, lang=lang)
    tts.save(TEMP_TTS_FILE)
    ffmpeg_conversion(TEMP_TTS_FILE, filename)
    remove(TEMP_TTS_FILE)
    return
