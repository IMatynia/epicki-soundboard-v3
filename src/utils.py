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