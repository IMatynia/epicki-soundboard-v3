from pathlib import Path


class TTSProvider:
    @staticmethod
    def get_all_languages() -> list[str]:
        ...

    @classmethod
    def generate_tts(cls, text: str, language: str, file_save_location: Path):
        ...