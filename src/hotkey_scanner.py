import pynput
from bitarray import bitarray
from logging import info
from src.hotkey_listener import HotkeyListener
from src.key import Key


class HotkeyScanner:
    _current_bitset = None
    _key_hook = None
    _scanned_keys = None

    @staticmethod
    def scan_keys_until_release_all():
        HotkeyListener.set_enabled(False)
        HotkeyScanner._scanned_keys = set()
        HotkeyScanner._current_bitset = bitarray(2**8)
        HotkeyScanner._current_bitset.setall(0)
        HotkeyScanner._key_hook = pynput.keyboard.Listener(
            HotkeyScanner._keyboard_hook_on_press,
            HotkeyScanner._keyboard_hook_on_release,
            True
        )
        HotkeyScanner._key_hook.start()
        HotkeyScanner._key_hook.join()
        HotkeyListener.set_enabled(True)
        return HotkeyScanner._scanned_keys

    @staticmethod
    def _keyboard_hook_on_press(key):
        if isinstance(key, pynput.keyboard.Key):
            code = key.value.vk
            name = key.name
        else:
            code = key.vk
            name = key.char

        # Numpad key
        if 96 <= code <= 105:
            name = f"Num {code - 96}"

        if name is None:
            name = f"key{code}"

        if not HotkeyScanner._current_bitset[code]:
            HotkeyScanner._scanned_keys.add(Key(name, code))
            HotkeyScanner._current_bitset[code] = True
            info(
                f"New press of {name}/{code}\n{HotkeyScanner._current_bitset}")
        return True

    @staticmethod
    def _keyboard_hook_on_release(key):
        return False
