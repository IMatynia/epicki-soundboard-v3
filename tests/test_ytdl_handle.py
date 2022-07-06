from src.youtube_dl_handle import download_media
from os import remove, path


def test_download():
    url = "https://youtu.be/dQw4w9WgXcQ"
    destination = "tests/test_data/rickroll.mp3"
    try:
        remove(destination)
    except FileNotFoundError:
        pass

    download_media(url, destination)
    assert path.exists(destination)
