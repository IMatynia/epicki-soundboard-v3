import pynput
from bitarray import bitarray
from src.keyboard_hotkey_callback import KeyboardHotkeyCallback


class HotkeyListener:
    """Static class managing hotkeys and keyboard hook.
    I implemented my own hotkey hooker because the default one from keyboard lib
    would only work if speciffically the given combination is provided.
    So in here if I set up a hotkey to keys "a" + "b", it will be detected 
    when I press "a" + "b" + "c" + "d" at the same time
    """
    _callbacks: "list" = None
    _current_bitset: "bitarray" = None
    _key_hook = None
    _enabled: "bool" = True
    _initialized: "bool" = False

    @staticmethod
    def init():
        """Initializes the listener
        """
        HotkeyListener._callbacks = []
        HotkeyListener._current_bitset = bitarray(2**8)
        HotkeyListener._current_bitset.setall(0)
        HotkeyListener._key_hook = pynput.keyboard.Listener(
            HotkeyListener._keyboard_hook_on_press,
            HotkeyListener._keyboard_hook_on_release
        )
        HotkeyListener._key_hook.start()
        HotkeyListener._enabled = True
        HotkeyListener._initialized = True

    @staticmethod
    def add_hotkey(keys, callback, args=None):
        """Adds the hotkey to the listener

        Args:
            keys (iterable): iterable with key names
            callback (function): callback to call if the combination is pressed
            args (list): arguments to call callback with
        """
        if not HotkeyListener._initialized:
            HotkeyListener.init()
        HotkeyListener._callbacks.append(
            KeyboardHotkeyCallback(keys, callback, args))

    @staticmethod
    def remove_all():
        """Removes all callbacks and hotkeys
        """
        if not HotkeyListener._initialized:
            HotkeyListener.init()
        HotkeyListener._callbacks.clear()

    @staticmethod
    def set_enabled(b):
        """Can allow for temporary suspention of all hotkeys

        Args:
            b (bool): should it work?
        """
        if not HotkeyListener._initialized:
            HotkeyListener.init()
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
        if not HotkeyListener._initialized:
            return
        HotkeyListener.remove_all()
        HotkeyListener._key_hook.stop()
