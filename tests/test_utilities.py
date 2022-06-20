from src.utils import check_if_program_present_in_path
from src.gtts_handle import generate_tts_ogg

def test_check_program():
    assert check_if_program_present_in_path("ffmpeg")
    assert check_if_program_present_in_path("youtube-dl")
    assert not check_if_program_present_in_path("googas")

def test_generate_tts_ogg():
    generate_tts_ogg("hi my name is bob and im your virtual assistant!", "en", "gtts_test_output.ogg")