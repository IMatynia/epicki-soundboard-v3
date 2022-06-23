from src.audio_hotkey import AudioHotkey, AudioHotkeyList, HotkeyCollisionError
import pytest


def test_simple_hotkey():
    hk = AudioHotkey(set(["a", "b", "c"]), "epic_battle_music.ogg", 3)
    assert hk.get_filename() == "epic_battle_music.ogg"
    assert hk.get_keys() == set(["a", "b", "c"])
    assert hk.get_page() == 3


def test_simple_hotkey_list():
    hkl = AudioHotkeyList(100)
    assert hkl.get_max_pages() == 100

    hk = AudioHotkey(set(["a", "b", "c"]), "epic_battle_music.ogg", 3)
    hkl.add_hotkey(hk)
    assert hkl.check_collision(hk)
    assert hkl.get_page(3) == [hk]
    assert hkl.get_page(1) == []

    with pytest.raises(HotkeyCollisionError):
        hkl.add_hotkey(hk)

    hkl.remove_hotkey(hk)
    assert not hkl.check_collision(hk)


def test_save_load_purge_list():
    init_list = [
        {"keys": ["*", "1"], "filename":"sogga.ogg", "page":0},
        {"keys": ["*", "2"], "filename":"floppa.ogg", "page":0},
        {"keys": ["*", "3"], "filename":"spingus.ogg", "page":0},
        {"keys": ["*", "1"], "filename":"sogga.ogg", "page":1}
    ]

    hkl = AudioHotkeyList()
    hkl.load_from_list(init_list)

    assert len(hkl.get_page(0)) == 3
    assert len(hkl.get_page(1)) == 1

    assert len(hkl.save_to_list()) == 4

    hkl.purge_data()
    assert len(hkl.get_page(0)) == 0
    assert len(hkl.get_page(1)) == 0
    hkl.add_hotkey(AudioHotkey(set(["*", "1"]), "sogga.ogg", 0))
    assert hkl.get_page(0) == [AudioHotkey(set(["*", "1"]), "sogga.ogg", 0)]
