import re

try:
    import rtyaml as yaml
except ImportError:
    import yaml


def load_from_comments(text):

    result = {}
    blocks = re.findall(r'^(\s*#.*?)\n(?:\w|$)', text, re.DOTALL | re.MULTILINE)

    for block in blocks:
        block_lines = block.splitlines()

        while (len(block_lines) > 0) and (':' not in block_lines[0]):
            block_lines.pop(0)

        while (len(block_lines) > 0):
            try:
                block = '\n'.join(block_lines)
                result.update(yaml.load(block.replace('#', '')))
                break
            except Exception as e:
                block_lines.pop()

    return result
