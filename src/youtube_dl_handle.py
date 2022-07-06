import subprocess


def download_media(url, destination_file: "str", callback=None):
    """Downloads the media from given URL and also pipes status into callback.
    This function is blocking. It will await completion of the download.
    The media will be downloaded in MP3 format.

    Args:
        url (str): media adress
        destination_file (str): destination
        callback (function): takes one string argument, the status (optional)
    """
    command = [
        "youtube-dl",
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
