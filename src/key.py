
class Key:
    """Represents a single key, contains a display name and a vk code
    """

    def __init__(self, name: "str" = None, vk: "int" = None) -> None:
        self.name = name
        self.vk = vk

    def load_from_dict(self, dict: "dict"):
        self.name = dict["name"]
        self.vk = dict["vk"]

    def save_to_dict(self):
        out = {
            "name": self.name,
            "vk": self.vk
        }
        return out

    def __str__(self) -> str:
        return f"{self.name} ({self.vk})"

    def __hash__(self) -> int:
        return hash((self.name, self.vk))

    def __eq__(self, other) -> bool:
        return other.name == self.name and other.vk == self.vk

    def __gt__(self, other) -> bool:
        return self.name > other.name


def keys_to_string(key_set: "set"):
    """Converts keys into a readable, non-debug string

    Args:
        key_set (set): set of keys

    Returns:
        str: string representation
    """
    return " + ".join([key.name for key in sorted(list(key_set))])
