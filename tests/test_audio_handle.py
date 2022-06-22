from time import sleep
import src.audio_handle as audio
from src.settings import Settings


def test_playback_play_and_stop_single():
    opt = Settings()
    opt.set_additional_device("default", audio.sounddevice.default.device)
    opt.set_play_on_main(False)
    th = audio.MultiAudioPlayThread("sigma.ogg", opt)
    th.start()
    sleep(2)
    th.stop_this()

    th = audio.MultiAudioPlayThread("sigma.ogg", opt)
    th.start()
    sleep(4)
    audio.stop_all_sounds()
    pass
