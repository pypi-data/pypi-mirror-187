import textwrap

def wrap(text, **kwargs):
    text = text.splitlines()
    text = [textwrap.fill(line, **kwargs) for line in text]
    return '\n'.join(text)