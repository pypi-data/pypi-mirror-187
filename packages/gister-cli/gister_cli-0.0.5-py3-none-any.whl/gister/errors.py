def get_error_name(error):
    error_type = type(error)
    if error_type.__module__ in ['__main__', 'builtins']:
        return error_type.__name__
    else:
        return f'{error_type.__module__}.{error_type.__name__}'


class Error(Exception):
    """Base class for all exceptions"""


class ContextError(Error):
    """Error in context"""


class HandledError(Error):
    """Error that has already been saved to errors context collection"""


class KeyInContextHasNoValueError(ContextError):
    """context[key] doesn't have a value."""


class KeyNotInContextError(ContextError, KeyError):
    """Key not found in context."""

    def __str__(self):
        """Avoid KeyError custom error formatting."""
        return super(Exception, self).__str__()


class FileTemplateError(Error):
    """Error processing template"""
