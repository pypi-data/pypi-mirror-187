from gister.git.environment import change_env


def main(git_env_change=None):
    if git_env_change is not None:
        change_env(git_env_change)
