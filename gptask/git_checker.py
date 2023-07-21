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
    Checks if the file has any uncommited changes or unstaged changes
    """
    has_commited_changes = subprocess.call(['git', 'diff-index', '--quiet', 'HEAD', '--', file], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) == 1
    has_unstaged_changes = subprocess.call(['git', 'diff-files', '--quiet', '--', file], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) == 1
    has_cached_changes = subprocess.call(['git', 'diff-index', '--quiet', '--cached', 'HEAD', '--', file], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) == 1
    return has_commited_changes or has_unstaged_changes or has_cached_changes


