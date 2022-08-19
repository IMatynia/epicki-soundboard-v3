import subprocess
from logging import info
from src.utils import check_if_program_present_in_path


class FFMPEGNotInPathError(Exception):
    def __init__(self) -> None:
        super().__init__("FFMPEG was not found in path!")


class FFMPEGRuntimeError(Exception):
    def __init__(self) -> None:
        super().__init__("Runtime FFMPEG error occured")


def ffmpeg_conversion(in_file: "str", out_file: "str", params: list = None) -> "int":
    """Converts files between audio-visual formats

    Args:
        in_file (str): source path
        out_file (str): destination path
        params (list, optional): Additional ffmpeg call params. Defaults to None.

    Raises:
        FFMPEGNotInPathError: if ffmpeg is not available in path

    Returns:
        int: ffmpeg call return value (0 - no errors)
    """
    if not check_if_program_present_in_path("ffmpeg"):
        raise FFMPEGNotInPathError()

    params = [] if params is None else params

    info(f"Converting {in_file} to {out_file} with [{params}] parameters")
    command = [
        "ffmpeg",
        "-i",
        f"{in_file}",
        *params,
        "-y",
        "-vn",
        f"{out_file}"
    ]
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    ret_val = subprocess.Popen(command, startupinfo=startupinfo).wait()

    if not ret_val == 0:
        raise FFMPEGRuntimeError()
