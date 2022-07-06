from src.utils import check_if_program_present_in_path, get_shortened_filename


def test_check_program():
    assert check_if_program_present_in_path("ffmpeg")
    assert check_if_program_present_in_path("youtube-dl")
    assert not check_if_program_present_in_path("googas")


def test_filename_shortner():
    assert get_shortened_filename("boss baby.mp3") == "boss baby.mp3"
    assert get_shortened_filename(
        "some folderino/opa gandam style.wav") == "some folderino/opa gandam style.wav"
    assert get_shortened_filename(
        "priest/king/aristocrat/slave.mp4.ogg.wav.ogg") == ".../aristocrat/slave.mp4.ogg.wav.ogg"
