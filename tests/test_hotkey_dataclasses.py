from src.audio_hotkey import AudioHotkey, AudioHotkeyList, HotkeyCollisionError
from src.keyboard_hotkeys import Key
import pytest


def test_key_class():
    k = Key("a", 1)
    assert k.name == "a"
    assert k.scan_code == 1
    assert str(k) == "a (1)"


def test_simple_hotkey():
    keys = set([
        Key("a", 1),
        Key("b", 2),
        Key("c", 3)
    ])
    hk = AudioHotkey(keys, "epic_battle_music.ogg", 3)
    assert hk.get_filename() == "epic_battle_music.ogg"
    assert hk.get_keys() == keys
    assert hk.get_page() == 3


def test_hotkey_compare():
    keys1 = set([
        Key("a", 1),
        Key("b", 2),
        Key("c", 3)
    ])

    keys2 = set([
        Key("g", 6),
        Key("e", 5),
        Key("f", 4)
    ])

    hk1 = AudioHotkey(keys1, "bingus.ogg", 0)
    hk2 = AudioHotkey(keys2, "bingus.ogg", 1)

    assert not hk1 == hk2

    hk2.set_keys(keys1)
    assert not hk1 == hk2

    hk2.set_page(0)
    assert hk1 == hk2

    hk2.set_filename("spoingus.ogg")
    assert hk1 == hk2


def test_simple_hotkey_list():
    hkl = AudioHotkeyList(100)
    assert hkl.get_max_pages() == 100

    keys = set([
        Key("a", 1),
        Key("b", 2),
        Key("c", 3)
    ])
    hk = AudioHotkey(keys, "epic_battle_music.ogg", 3)
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
        {"keys": [{"name": "*", "scan_code": 1}, {"name": "1",
                                                  "scan_code": 2}], "filename": "sogga.ogg", "page": 0},
        {"keys": [{"name": "*", "scan_code": 1}, {"name": "2",
                                                  "scan_code": 3}], "filename": "floppa.ogg", "page": 0},
        {"keys": [{"name": "*", "scan_code": 1}, {"name": "3",
                                                  "scan_code": 4}], "filename": "spingus.ogg", "page": 0},
        {"keys": [{"name": "*", "scan_code": 1}, {"name": "1",
                                                  "scan_code": 2}], "filename": "sogga.ogg", "page": 1}
    ]

    hkl = AudioHotkeyList()
    hkl.load_from_list(init_list)

    assert len(hkl.get_page(0)) == 3
    assert len(hkl.get_page(1)) == 1

    assert len(hkl.save_to_list()) == 4

    hkl.purge_data()
    assert len(hkl.get_page(0)) == 0
    assert len(hkl.get_page(1)) == 0
    hkl.add_hotkey(AudioHotkey(
        set([Key("*", 1), Key("1", 2)]), "sogga.ogg", 0))
    page_0 = hkl.get_page(0)
    assert page_0 == [AudioHotkey(
        set([Key("*", 1), Key("1", 2)]), "sogga.ogg", 0)]


def test_hash_audio_hotkey():
    key1 = Key("a", 1)
    key2 = Key("b", 2)
    key3 = Key("c", 3)
    a = AudioHotkey({key1, key2}, "bingus.ogg", 0)
    b = AudioHotkey({key3, key2}, "spoingus.ogg", 1)

    s = {a, b}
    assert a in s
    assert b in s
