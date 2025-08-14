from pathlib import Path

class AudioCodecsProvider:
    @classmethod
    def convert_audio_format(cls, source_path: Path, destination_path: Path, additional_params: dict | None = None):
        ...

    @classmethod
    def load_audio_with_supported_format(cls, audio_source: Path):
        ...
