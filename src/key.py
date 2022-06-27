
class Key:
    def __init__(self, name=None, vk=None) -> None:
        self.name = name
        self.vk = vk

    def load_from_dict(self, dict):
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


def keys_to_string(key_set):
    return " + ".join([key.name for key in sorted(list(key_set))])
