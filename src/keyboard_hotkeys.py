from logging import info
from time import sleep, time
import keyboard
from bitarray import bitarray


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
        return hash(self.name) + hash(self.scan_code)

    def __eq__(self, other) -> bool:
        return other.name == self.name and other.scan_code == self.scan_code

    def __gt__(self, other) -> bool:
        return self.name > other.name


def keys_to_string(key_set):
    return " + ".join([key.name for key in sorted(list(key_set))])


class HoldYourHorses:
    def __init__(self, delay=10) -> None:
        self._delay = delay
        self._wait_until = [0] * 256

    def try_pressing_again(self, scan_code):
        now = time()
        can_continue = False
        if now > self._wait_until[scan_code]:
            can_continue = True

        self._wait_until[scan_code] = now + self._delay/1000
        return can_continue


class KeyScanner:
    _scan_hook_running = False
    _n_of_pressed_keys = 0
    _all_keys = set()
    _scan_hook = None
    _awaiting = HoldYourHorses()

    @staticmethod
    def _press_callback(event):
        new_key = Key(event.name, event.scan_code)
        if event.event_type == "down" \
                and new_key not in KeyScanner._all_keys \
                and KeyScanner._awaiting.try_pressing_again(event.scan_code):
            info(
                f"DOWN {event.scan_code} | Currently pressed: {KeyScanner._n_of_pressed_keys}")
            KeyScanner._n_of_pressed_keys += 1
            KeyScanner._all_keys.add(new_key)
        elif KeyScanner._awaiting.try_pressing_again(event.scan_code):
            info(
                f"UP {event.scan_code} | Currently pressed: {KeyScanner._n_of_pressed_keys}")
            KeyScanner._n_of_pressed_keys -= 1

        if KeyScanner._n_of_pressed_keys <= 0:  # User stopped pressing any buttons, scan complete
            KeyScanner._scan_hook_running = False
            keyboard.unhook(KeyScanner._scan_hook)
        return

    @staticmethod
    def get_keys():
        KeyScanner._scan_hook_running = True
        KeyScanner._scan_hook = keyboard.hook(KeyScanner._press_callback, True)

        timeout = 30
        while KeyScanner._scan_hook_running and timeout > 0:
            sleep(0.2)
            timeout -= 0.2

        if timeout <= 0:
            raise Exception("Hotkey scanning timeout!")

        detail = " ".join([str(key) for key in KeyScanner._all_keys])
        info(f"Scanned keys: {detail}")
        return KeyScanner._all_keys


def scan_pressed_keys():
    return KeyScanner.get_keys()


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

    @staticmethod
    def _keys_to_bitset(keys):
        bitmask = bitarray(2**8)
        bitmask.setall(0)
        for key in keys:
            bitmask[key.scan_code] = True
        return bitmask

    @staticmethod
    def _run_matching_hotkey():
        for callback in HotkeyManager._callbacks:
            # Bitmap is matching
            if HotkeyManager._bitset & callback.key_bitmap == callback.key_bitmap:
                callback.run()
