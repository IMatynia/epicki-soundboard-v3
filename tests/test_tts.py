from src.gtts_handle import generate_tts_ogg
from os import path, remove


def test_generate_tts_ogg():
    destination = "./tests/test_data/gtts_test_output.ogg"
    try:
        remove(destination)
    except FileNotFoundError:
        pass
    generate_tts_ogg(
        "hi my name is bob and im your virtual assistant!", "en", destination)
    assert path.exists(destination)
