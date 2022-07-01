import subprocess
from logging import info
from src.utils import check_if_program_present_in_path


class FFMPEGNotInPathError(Exception):
    def __init__(self) -> None:
        super().__init__("FFMPEG was not found in path!")


def ffmpeg_conversion(in_file: "str", out_file: "str", params: "str" = None) -> "int":
    """Converts files between audio-visual formats

    Args:
        in_file (str): source path
        out_file (str): destination path
        params (str, optional): Additional ffmpeg call params. Defaults to None.

    Raises:
        FFMPEGNotInPathError: if ffmpeg is not available in path

    Returns:
        int: ffmpeg call return value (0 - no errors)
    """
    if not check_if_program_present_in_path("ffmpeg"):
        raise FFMPEGNotInPathError()

    info(f"Converting {in_file} to {out_file} with [{params}] parameters")
    command = [
        "ffmpeg",
        "-y",
        "-vn",
        "-i",
        f"{in_file}",
        f"{out_file}"
    ]

    if params:
        command.insert(2, params)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(command, startupinfo=startupinfo).wait()
