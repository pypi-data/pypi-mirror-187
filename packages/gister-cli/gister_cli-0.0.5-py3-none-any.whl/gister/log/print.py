from gister.utils.text import wrap


class PrintLog:

    def info(message: str):
        print(f"\033[1;34;10m{wrap(message)}\033[0m\n")

    def success(message: str):
        print(f"\033[1;32;10m{wrap(message)} \U0001F44D\033[0m\n")

    def warning(message: str):
        print(f"\033[1;33;10m{wrap(message)} \U0001F9DF\033[0m\n")

    def error(message: str):
        print(f"\033[1;31;10m{wrap(message)} \U0001F525\033[0m\n")
