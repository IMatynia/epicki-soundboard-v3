import pynput
from bitarray import bitarray
from src.config.config import KeyPress
from src.hotkey_listener import HotkeyListener
from pynput.keyboard import Key, KeyCode


class HotkeyScanner:
    def __init__(self, callback):
        """Creates a scanner object

        Args:
            callback (function): called when the scanning is finished, takes one argument - scanned keys
        """
        self._current_bitset = bitarray(2**8)
        self._key_hook = pynput.keyboard.Listener(
            self._keyboard_hook_on_press, self._keyboard_hook_on_release, True
        )
        self._callback = callback
        self._scanned_keys = set()

    def start(self):
        """Starts the hotkeys scanning. When completed, the callback will be called. Disables hotkeys temporarily."""
        HotkeyListener.set_enabled(False)
        self._current_bitset.setall(0)
        self._key_hook.start()

    def await_completion(self):
        self._key_hook.join()

    def _keyboard_hook_on_press(self, key: Key | KeyCode | None) -> None:
        if isinstance(key, Key):
            code = key.value.vk or 0
            name = key.name
        elif isinstance(key, KeyCode):
            code = key.vk or 0
            name = key.char
        else:
            code = 0
            name = "N/A"

        # Numpad key
        if 96 <= code <= 105:
            name = f"Num {code - 96}"

        if name is None:
            name = f"key{code}"

        if not self._current_bitset[code]:
            self._scanned_keys.add(KeyPress(name=name, vk=code))
            self._current_bitset[code] = True

    def _keyboard_hook_on_release(self, _: Key | KeyCode | None):
        """When scanning is complete (any of the keys was lifted) call the callback with scanned keys"""
        HotkeyListener.set_enabled(True)
        if self._callback:
            self._callback(self._scanned_keys)
        
        self._key_hook.stop()
