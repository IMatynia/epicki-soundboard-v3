from logging import info
import subprocess
import re


class YTDLRuntimeError(Exception):
    def __init__(self, error_message) -> None:
        super().__init__(f"YTDL runtime error\n{error_message}")


def download_media(url, destination_file: "str", custom_args: list = None, callback=None):
    """Downloads the media from given URL and also pipes status into callback.
    This function is blocking. It will await completion of the download.
    The media will be downloaded in MP3 format.

    Args:
        url (str): media adress
        destination_file (str): destination
        custom_args (list): list of custom arguments, if none default ones will be used (audio extract)
        callback (function): takes one string argument, the status (optional)
    """
    custom_args = [] if custom_args is None or custom_args[0] == "" else custom_args

    command = [
        "youtube-dl",
        *custom_args,
        "-x",
        "--audio-format",
        "mp3",
        "--newline",
        "--prefer-ffmpeg",
        url,
        "-o",
        destination_file]

    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if callback is None:
        return proc.wait()
    else:
        for line in proc.stdout:
            line = str(line)[2:-1]
            info(line)
            if re.findall("ERROR:", line):
                raise YTDLRuntimeError(line)
            callback(line)
