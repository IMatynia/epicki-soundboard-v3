from logging import info
from time import sleep
import keyboard
from bitarray import bitarray

_SCAN_HOOK_RUNNING = False


def scan_pressed_keys():
    global _SCAN_HOOK_RUNNING
    all_keys = set()

    def press_callback(event):
        global _SCAN_HOOK_RUNNING
        if event.scan_code == 1:  # User pressed ESC
            _SCAN_HOOK_RUNNING = False
            keyboard.unhook(press_callback)
            return
        # Save the key name (can be converted into scan code)
        all_keys.add(event.name)

    _SCAN_HOOK_RUNNING = True
    keyboard.hook(press_callback, True)

    # Await completion
    timeout = 30
    while _SCAN_HOOK_RUNNING and timeout > 0:
        sleep(0.2)
        timeout -= 0.2

    # Timeout
    if timeout <= 0:
        raise Exception("Hotkey scanning timeout!")

    info("Key scanning complete!")
    return all_keys


class HotkeyCallback:
    def __init__(self, key_bitmap, callback, args) -> None:
        """Data class storing information about a hotkey combination

        Args:
            key_bitmap (bitarray): stores which keycodes should be pressed
                to activate callback
            callback (function): the callback to run
            args (list): argument list to run callback with
        """
        self.key_bitmap = key_bitmap
        self.callback = callback
        self.args = args

    def run(self):
        self.callback(*self.args)


class HotkeyManager:
    """Static class managing hotkeys and keyboard hook.
    I implemented my own hotkey hooker because the default one from keyboard lib
    would only work if speciffically the given combination is provided.
    So in here if I set up a hotkey to keys "a" + "b", it will be detected 
    when I press "a" + "b" + "c" + "d" at the same time

    Returns:
        _type_: _description_
    """
    _callbacks = None
    _bitset = None
    _key_hook = None
    _enabled = True

    @staticmethod
    def init():
        HotkeyManager._callbacks = []
        HotkeyManager._bitset = bitarray(2**8)
        HotkeyManager._bitset.setall(0)
        HotkeyManager._key_hook = keyboard.hook(
            HotkeyManager._keyboard_hook_on_event)
        HotkeyManager._enabled = True

    @staticmethod
    def add_hotkey(keys, callback, args):
        """Adds the hotkey to the listener

        Args:
            keys (iterable): iterable with key names
            callback (function): callback to call if the combination is pressed
            args (list): arguments to call callback with
        """
        bitset = HotkeyManager._keys_to_bitset(keys)
        HotkeyManager._callbacks.append(HotkeyCallback(bitset, callback, args))

    @staticmethod
    def remove_all():
        """Removes all callbacks and hotkeys
        """
        HotkeyManager._callbacks.clear()

    @staticmethod
    def set_enabled(b):
        """Can allow for suspention of all hotkeys

        Args:
            b (bool): should it work?
        """
        HotkeyManager._enabled = b

    @staticmethod
    def _keyboard_hook_on_event(event):
        code = event.scan_code
        type = event.event_type

        if type == "down":
            HotkeyManager._bitset[code] = True
            if HotkeyManager._enabled:
                HotkeyManager._run_matching_hotkey()
        else:
            HotkeyManager._bitset[code] = False
            info(f"{code} Released!")

    @staticmethod
    def _keys_to_bitset(keys):
        bitmask = bitarray(2**8)
        bitmask.setall(0)
        for key in keys:
            bitmask[keyboard.key_to_scan_codes(key)[0]] = True
        return bitmask

    @staticmethod
    def _run_matching_hotkey():
        for callback in HotkeyManager._callbacks:
            # Bitmap is matching
            if HotkeyManager._bitset & callback.key_bitmap == callback.key_bitmap:
                callback.run()
