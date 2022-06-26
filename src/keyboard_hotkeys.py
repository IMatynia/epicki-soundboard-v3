import pynput
from bitarray import bitarray
from logging import info
# TODO: put these classes into separate files


class Key:
    def __init__(self, name=None, scan_code=None) -> None:
        self.name = name
        self.scan_code = scan_code

    def load_from_dict(self, dict):
        self.name = dict["name"]
        self.scan_code = dict["scan_code"]

    def save_to_dict(self):
        out = {
            "name": self.name,
            "scan_code": self.scan_code
        }
        return out

    def __str__(self) -> str:
        return f"{self.name} ({self.scan_code})"

    def __hash__(self) -> int:
        return hash((self.name, self.scan_code))

    def __eq__(self, other) -> bool:
        return other.name == self.name and other.scan_code == self.scan_code

    def __gt__(self, other) -> bool:
        return self.name > other.name


def keys_to_string(key_set):
    return " + ".join([key.name for key in sorted(list(key_set))])

# TODO: make this work with a callback ("on scan complete etc")
class HotkeyScanner:
    _current_bitset = None
    _key_hook = None
    _scanned_keys = None

    @staticmethod
    def scan_keys_until_release_all():
        HotkeyScanner._scanned_keys = set()
        HotkeyScanner._current_bitset = bitarray(2**8)
        HotkeyScanner._current_bitset.setall(0)
        HotkeyScanner._key_hook = pynput.keyboard.Listener(
            HotkeyScanner._keyboard_hook_on_press,
            HotkeyScanner._keyboard_hook_on_release
        )
        HotkeyScanner._key_hook.start()
        HotkeyScanner._key_hook.join()
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


class KeyboardHotkeyCallback:
    def __init__(self, keys, callback, args) -> None:
        """Data class storing information about a hotkey combination

        Args:
            keys (iterable): keys to press to activate callback
            callback (function): the callback to run
            args (list): argument list to run callback with
        """
        self.key_bitmap = KeyboardHotkeyCallback.keys_to_bitset(keys)
        self.callback = callback
        self.args = args

    def run(self):
        self.callback(*self.args)

    @staticmethod
    def keys_to_bitset(keys):
        bitmask = bitarray(2**8)
        bitmask.setall(0)
        for key in keys:
            bitmask[key.scan_code] = True
        return bitmask


class HotkeyListener:
    """Static class managing hotkeys and keyboard hook.
    I implemented my own hotkey hooker because the default one from keyboard lib
    would only work if speciffically the given combination is provided.
    So in here if I set up a hotkey to keys "a" + "b", it will be detected 
    when I press "a" + "b" + "c" + "d" at the same time

    Returns:
        _type_: _description_
    """
    _callbacks = None
    _current_bitset = None
    _key_hook = None
    _enabled = True

    @staticmethod
    def init():
        HotkeyListener._callbacks = []
        HotkeyListener._current_bitset = bitarray(2**8)
        HotkeyListener._current_bitset.setall(0)
        HotkeyListener._key_hook = pynput.keyboard.Listener(
            HotkeyListener._keyboard_hook_on_press,
            HotkeyListener._keyboard_hook_on_release
        )
        HotkeyListener._key_hook.start()
        HotkeyListener._enabled = True

    @staticmethod
    def add_hotkey(keys, callback, args):
        """Adds the hotkey to the listener

        Args:
            keys (iterable): iterable with key names
            callback (function): callback to call if the combination is pressed
            args (list): arguments to call callback with
        """
        HotkeyListener._callbacks.append(
            KeyboardHotkeyCallback(keys, callback, args))

    @staticmethod
    def remove_all():
        """Removes all callbacks and hotkeys
        """
        HotkeyListener._callbacks.clear()

    @staticmethod
    def set_enabled(b):
        """Can allow for suspention of all hotkeys

        Args:
            b (bool): should it work?
        """
        HotkeyListener._enabled = b

    @staticmethod
    def _keyboard_hook_on_press(key):

        if isinstance(key, pynput.keyboard.Key):
            code = key.value.vk
        else:
            code = key.vk

        if HotkeyListener._enabled and not HotkeyListener._current_bitset[code]:
            HotkeyListener._current_bitset[code] = True
            HotkeyListener._run_matching_hotkey()
        return True

    @staticmethod
    def _keyboard_hook_on_release(key):
        if isinstance(key, pynput.keyboard.Key):
            code = key.value.vk
        else:
            code = key.vk
        HotkeyListener._current_bitset[code] = False
        return True

    @staticmethod
    def _run_matching_hotkey():
        for callback in HotkeyListener._callbacks:
            # Bitmap is matching
            if HotkeyListener._current_bitset & callback.key_bitmap == callback.key_bitmap:
                callback.run()
