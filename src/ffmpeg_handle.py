from distutils.log import error
import subprocess
from logging import info
from src.utils import check_if_program_present_in_path


class FFMPEGNotInPathError(Exception):
    def __init__(self) -> None:
        super().__init__("FFMPEG was not found in path!")


class FFMPEGRuntimeError(Exception):
    def __init__(self, return_value, error_message) -> None:
        super().__init__(
            f"Runtime FFMPEG error occured\n-------\nReturn code: {return_value:X}\n-------\nError message:\n{error_message}")


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

    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        raise FFMPEGRuntimeError(e.returncode, e.output)
