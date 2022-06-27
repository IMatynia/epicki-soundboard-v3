import pynput
from bitarray import bitarray


class KeyboardHotkeyCallback:
    def __init__(self, keys, callback, args=None) -> None:
        """Data class storing information about a hotkey combination

        Args:
            keys (iterable): keys to press to activate callback
            callback (function): the callback to run
            args (list): argument list to run callback with
        """
        self.key_bitmap = KeyboardHotkeyCallback.keys_to_bitset(keys)
        self.callback = callback
        self.args = args if args else []

    def run(self):
        self.callback(*self.args)

    @staticmethod
    def keys_to_bitset(keys):
        bitmask = bitarray(2**8)
        bitmask.setall(0)
        for key in keys:
            bitmask[key.vk] = True
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
    def add_hotkey(keys, callback, args=None):
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

    @staticmethod
    def stop():
        HotkeyListener.remove_all()
        HotkeyListener._key_hook.stop()
