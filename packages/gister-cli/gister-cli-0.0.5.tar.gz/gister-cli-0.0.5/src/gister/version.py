import platform

__version__ = '0.0.5'


def get_version():
    return (f'gister: {__version__}\n'
            f'python: {platform.python_version()}')
