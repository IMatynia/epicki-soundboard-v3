import subprocess
from logging import info
from src.utils import check_if_program_present_in_path


class FFMPEGNotInPathError(Exception):
    pass


def ffmpeg_conversion(in_file, out_file, params=""):
    if not check_if_program_present_in_path("ffmpeg"):
        raise FFMPEGNotInPathError()

    info(f"Converting {in_file} to {out_file} with [{params}] parameters")
    # TODO: custom params support
    command = [
        "ffmpeg",
        "-y",
        "-vn",
        "-i",
        f"{in_file}",
        f"{out_file}"
    ]
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(command, startupinfo=startupinfo).wait()
