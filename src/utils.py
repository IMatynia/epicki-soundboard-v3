import subprocess


def check_if_program_present_in_path(program):
    """Checks if the program is present in path (windows only)

    Args:
        program (str): the program name

    Returns:
        bool: is it in path?
    """
    proc = subprocess.Popen(f"where {program}", stdout=subprocess.PIPE)
    output = proc.stdout.read()
    return not output == b''


def get_shortened_filename(filename: "str") -> "str":
    """Returns a more digestable filename

    Args:
        filename (str): full path to a file

    Returns:
        str: shortened path with just one folder preceeding the file
    """
    splitted = filename.split("/")
    if len(splitted) == 1:
        return splitted[0]
    out = ".../" if len(splitted) > 2 else ""
    out += f"{splitted[-2]}/{splitted[-1]}"
    return out
