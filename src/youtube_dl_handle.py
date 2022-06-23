import subprocess


def download_media(url, destination_file, callback):
    """Downloads the media from given URL and also pipes status into callback

    Args:
        url (str): media adress
        destination_file (str): destination
        callback (function): takes one string argument, the status
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
    for line in proc.stdout:
        callback(str(line)[2:-1])
