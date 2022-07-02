from os import remove
from src.ffmpeg_handle import ffmpeg_conversion
from src.constants import TEMP_TTS_FILE_MP3
import gtts

_LANGUAGE_LIST = list(gtts.lang.tts_langs())


class InvalidLanguageError(Exception):
    pass


def get_languages() -> "list":
    """Returns a list of language codes supported by google tts

    Returns:
        list: the language codes
    """
    return _LANGUAGE_LIST


def generate_tts_ogg(text: "str", lang: "str", filename: "str") -> "int":
    """Creates a google TTS file of a given filename. FFMPEG required

    Args:
        text (str): the text to speak
        lang (str): language code (only the ones accepted by gtts are allowed)
        filename (str): destination file (extension must be provided)
    
    Returns:
        int: ffmpeg conversion return value
    """
    if lang not in get_languages():
        raise InvalidLanguageError()

    tts = gtts.gTTS(text=text, lang=lang)
    tts.save(TEMP_TTS_FILE_MP3)
    ret_val = ffmpeg_conversion(TEMP_TTS_FILE_MP3, filename)
    remove(TEMP_TTS_FILE_MP3)
    return ret_val
