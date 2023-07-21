import subprocess

def is_staged(file: str):
    """
    First checks if git is being used then checks if the file has no staged changes
    """
    if not is_git_repo():
        return False

    return any_changes(file)


def is_git_repo():
    """
    Checks if the current directory is a git repo
    """
    return subprocess.call(['git', 'branch'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) == 0

def any_changes(file: str):
    """
    Checks if the file has any uncommitted changes or unstaged changes
    """
    status = subprocess.check_output(['git', 'status', '--porcelain', file], text=True)

    # If there are any changes, the status command will print out lines starting
    # with 'M' (modified), 'A' (added), 'D' (deleted), etc.
    # If there are no changes, status will be an empty string.
    return bool(status.strip())