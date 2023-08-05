from gister.errors import (ContextError, KeyNotInContextError, KeyInContextHasNoValueError)


def assert_key_exists(obj, key, caller, parent=None):
    try:
        if key not in obj:
            if parent:
                msg = (f"context[{parent!r}][{key!r}] doesn't "
                       f"exist. It must exist for {caller}.")
            else:
                msg = (
                    f"context[{key!r}] doesn't exist. "
                    f"It must exist for {caller}."
                )
            raise KeyNotInContextError(msg)
    except TypeError as err:
        if parent:
            msg = (f"context[{parent!r}] must exist, be iterable and contain "
                   f"{key!r} for {caller}. {err}")
        else:
            msg = (f"context[{key!r}] must exist and be iterable for "
                   f"{caller}. {err}")
        raise ContextError(msg) from err


def assert_key_has_value(obj, key, caller, parent=None):
    assert_key_exists(obj, key, caller, parent)
    if obj[key] is None:
        if parent:
            msg = (f"context[{parent!r}][{key!r}] must have a value for "
                   f"{caller}.")
        else:
            msg = f"context[{key!r}] must have a value for {caller}."

        raise KeyInContextHasNoValueError(msg)


def assert_key_is_truthy(obj, key, caller, parent=None):
    assert_key_exists(obj, key, caller, parent)
    if not obj[key]:
        if parent:
            msg = (f"context[{parent!r}][{key!r}] must have a value for "
                   f"{caller}.")
        else:
            msg = f"context[{key!r}] must have a value for {caller}."

        raise KeyInContextHasNoValueError(msg)
