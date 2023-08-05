from pathlib import Path

from gister.errors import ContextError, FileTemplateError
from gister.log.print import PrintLog

""" Git template section
"""


def user_section(name="", email=""):
    return f'\
[user]\n\
  name="{name}"\n\
  email="{email}"'


def filter_section():
    return f'\n\
[filter "lfs"]\n\
  clean=git-lfs clean -- %f\n\
  smudge=git-lfs smudge -- %f\n\
  process=git-lfs filter-process\n\
  required=true\n'


def ssh_section():
    return f'\n\
[url "ssh://git@github.com/"]\n\
  insteadOf=https://github.com/\
  '


""" Process and Create template
"""


def process_template(template=""):
    try:
        if template == "":
            raise ContextError("Template must not empty")
        path = f"{Path.home()}/.gitconfig"
        with open(path, "w") as file:
            file.write(template)
            file.close()
            PrintLog.success("git environment switched!")

    except FileTemplateError:
        raise
