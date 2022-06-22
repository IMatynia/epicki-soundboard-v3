from logging import info
from time import sleep
import keyboard

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
