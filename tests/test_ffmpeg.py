from src.ffmpeg_handle import ffmpeg_conversion, FFMPEGRuntimeError
from os import remove, path
import pytest


def test_conversion_mp3_to_ogg():
    source = "./tests/test_data/welcome to 17.mp3"
    destination = "./tests/test_data/welcome to 17.ogg"

    try:
        remove(destination)
    except FileNotFoundError:
        pass

    assert ffmpeg_conversion(source, destination) == 0
    assert path.exists(destination)


def test_conversion_invalid_file():
    source = "./tests/test_data/zoomba.mp3"
    destination = "./tests/test_data/zoomba.ogg"

    with pytest.raises(FFMPEGRuntimeError):
        ffmpeg_conversion(source, destination)
    assert not path.exists(destination)
