from src.settings import Settings


def test_settings_init_save_load_default():
    sett = Settings()
    assert sett.get_additional_device() == None
    assert sett.get_window_h_pos() == 200
    assert sett.get_window_v_pos() == 200

    example = sett.save_to_dict()
    example["window_h_pos"] = 50
    sett.load_from_dict(example)

    assert sett.get_window_h_pos() == 50
