from pathlib import Path

def get_shortened_filename(filename: Path) -> "str":
    """Returns a more digestable filename

    Args:
        filename (str): full path to a file

    Returns:
        str: shortened path with just one folder preceeding the file
    """
    file_base = filename.stem
    parent_folder = filename.parent.stem
    return f"{file_base} ({parent_folder})"
