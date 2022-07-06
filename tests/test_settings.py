from src.settings import Settings
from src.audio_devices import InvalidDeviceNameError
from pytest import raises


def test_settings_init_save_load_default():
    sett = Settings()
    assert sett.get_additional_device() is None
    assert sett.get_window_h_pos() == 200
    assert sett.get_window_v_pos() == 200
    assert sett.get_play_on_main()
    assert not sett.get_is_singular()
    assert sett.get_tts_language() == "en"
    assert sett.get_additional_device_num() == -1

    example = sett.save_to_dict()
    assert len(example) == 14
    example["window_h_pos"] = 50
    sett.load_from_dict(example)
    assert sett.get_window_h_pos() == 50

    sett2 = Settings()
    example["additional_device"] = "this one does not exist, i am sure of that"
    with raises(InvalidDeviceNameError):
        sett2.load_from_dict(example)
