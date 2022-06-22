from src.hotkey import Hotkey, HotkeyList, HotkeyCollisionError
import pytest


def test_simple_hotkey():
    hk = Hotkey(set(["a", "b", "c"]), "epic_battle_music.ogg", 3)
    assert hk.get_filename() == "epic_battle_music.ogg"
    assert hk.get_keys() == set(["a", "b", "c"])
    assert hk.get_page() == 3


def test_simple_hotkey_list():
    hkl = HotkeyList()
    hk = Hotkey(set(["a", "b", "c"]), "epic_battle_music.ogg", 3)
    hkl.add_hotkey(hk)
    assert hkl.check_collision(hk)
    assert hkl.get_page(3) == [hk]
    assert hkl.get_page(1) == []

    with pytest.raises(HotkeyCollisionError):
        hkl.add_hotkey(hk)

    hkl.remove_hotkey(hk)
    assert not hkl.check_collision(hk)
