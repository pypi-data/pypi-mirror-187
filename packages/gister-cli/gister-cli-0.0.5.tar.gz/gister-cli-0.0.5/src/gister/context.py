from collections import namedtuple

from gister.errors import KeyInContextHasNoValueError, KeyNotInContextError
from gister.utils import asserts

ContextItemInfo = namedtuple('ContextItemInfo',
                             ['key',
                              'key_in_context',
                              'expected_type',
                              'is_expected_type',
                              'has_value'])


class Context(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pystring_globals = {}

    def __missing__(self, key):
        raise KeyNotInContextError(f"{key} not found in gister context.")

    def assert_child_key_has_value(self, parent, child, caller):
        asserts.assert_key_has_value(self, parent, caller)
        asserts.assert_key_has_value(self[parent], child, caller, parent)

    def assert_key_exists(self, key, caller):
        asserts.assert_key_exists(self, key, caller)

    def assert_key_has_value(self, key, caller):
        asserts.assert_key_has_value(self, key, caller)

    def assert_key_type_value(self, context_item, caller, extra_error_text=""):
        assert context_item, ("context_item parameter must be specified.")
        if extra_error_text is None or extra_error_text == '':
            append_error_text = ''
        else:
            append_error_text = f' {extra_error_text}'

        if not context_item["key_in_context"]:
            raise KeyNotInContextError(
                f'{caller} couldn\'t find '
                f'{context_item["key"]} in context.'
                f'{append_error_text}'
            )

        if not context_item["has_value"]:
            raise KeyInContextHasNoValueError(
                f'{caller} found {context_item["key"]} in '
                f'context but it doesn\'t have a value.'
                f'{append_error_text}'
            )
        if not context_item["is_expected_type"]:
            raise KeyInContextHasNoValueError(
                f'{caller} found {context_item["key"]} in context, but it\'s '
                f'not a {context_item["expected_type"]}.'
                f'{append_error_text}'
            )

    def assert_keys_exist(self, caller, *keys):
        assert keys, ("*keys parameter must be specified.")
        for key in keys:
            self.assert_key_exists(key, caller)

    def assert_keys_have_values(self, caller, *keys):
        for key in keys:
            self.assert_key_has_value(key, caller)

    def assert_child_keys_has_values(self, parent, child, keys, caller):
        for key in keys:
            self.assert_child_key_has_value(parent, key, caller)

    def assert_keys_type_value(self,
                               caller,
                               extra_error_text,
                               *context_items):

        assert context_items, ("context_items parameter must be specified.")

        for context_item in context_items:
            self.assert_key_type_value(context_item, caller, extra_error_text)

    def get_formatted(self, key):
        val = self[key]

        try:
            # any sort of complex type will work with recursive formatter.
            if val is None: raise KeyNotInContextError
            return val
        except KeyNotInContextError as err:
            # less cryptic error for end-user friendliness
            raise KeyNotInContextError(
                f'Unable to format \'{val}\' at context[\'{key}\'], '
                f'because {err}'
            ) from err
