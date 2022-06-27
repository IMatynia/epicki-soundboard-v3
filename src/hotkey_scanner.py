import pynput
from bitarray import bitarray
from logging import info
from src.hotkey_listener import HotkeyListener
from src.key import Key


class HotkeyScanner:
    def __init__(self, callback):
        """Creates a scanner object

        Args:
            callback (function): called when the scanning is finished, takes one argument - scanned keys
        """
        self._current_bitset = None
        self._key_hook = None
        self._callback = callback
        self._key_hook = None
        self._scanned_keys = None

    def start(self):
        """Starts the hotkeys scanning. When completed, the callback will be called
        """
        HotkeyListener.set_enabled(False)
        self._scanned_keys = set()
        self._current_bitset = bitarray(2**8)
        self._current_bitset.setall(0)
        self._key_hook = pynput.keyboard.Listener(
            self._keyboard_hook_on_press,
            self._keyboard_hook_on_release,
            True
        )
        self._key_hook.start()

    def await_completion(self):
        self._key_hook.join()

    def _keyboard_hook_on_press(self, key):
        """Add each keypress to the scanned keys set
        """
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

        if not self._current_bitset[code]:
            self._scanned_keys.add(Key(name, code))
            self._current_bitset[code] = True
            info(
                f"New press of {name}/{code}\n{self._current_bitset}")
        return True

    def _keyboard_hook_on_release(self, key):
        """When scanning is complete (any of the keys was lifted) call the callback with scanned keys
        """
        HotkeyListener.set_enabled(True)
        if self._callback:
            self._callback(self._scanned_keys)
        return False
