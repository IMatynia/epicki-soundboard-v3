from bitarray import bitarray


class KeyboardHotkeyCallback:
    """Data class storing information about a hotkey combination and
    the callback with arguments to call
    """

    def __init__(self, keys: "set", callback, args: "list" = None) -> None:
        """Create KeyboardHotkeyCallback instance

        Args:
            keys (set): keys to press to activate callback
            callback (function): the callback to run
            args (list): argument list to run callback with
        """
        self.key_bitmap = KeyboardHotkeyCallback.keys_to_bitset(keys)
        self.callback = callback
        self.args = args if args else []

    def run(self):
        """Calls the callback with args
        """
        self.callback(*self.args)

    @staticmethod
    def keys_to_bitset(keys: "set") -> "bitarray":
        """Converts a set of keys into a bitarray for HotkeyListener to read.
        Bits on indexes of Keys' VK codes are set to 1

        Args:
            keys (set): set of keys

        Returns:
            bitarray: result bitarray
        """
        bitmask = bitarray(2**8)
        bitmask.setall(0)
        for key in keys:
            bitmask[key.vk] = True
        return bitmask
