from optparse import Option
from src.options import Options

def test_options_init_save_load_default():
    opt = Options()
    assert opt.get_additional_device_name() == "no device"
    assert opt.get_window_h_pos() == 200
    assert opt.get_window_v_pos() == 200

    example = opt.save_to_dict()   
    example["additional_device_name"] = "magic speaker"
    opt.load_from_dict(example)

    assert opt.get_additional_device_name() == "magic speaker"