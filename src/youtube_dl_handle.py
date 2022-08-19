import subprocess


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

    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    if callback is None:
        return proc.wait()
    else:
        for line in proc.stdout:
            callback(str(line)[2:-1])
