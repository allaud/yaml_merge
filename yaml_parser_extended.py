import re

try:
    import rtyaml as yaml
except ImportError:
    import yaml


y = """
test1: 1213123
test2: asdasdsd
#test3: asdasdsd
"""

yy = """
#dsdf
#sdsd: 32323
#dfdfd
test: 123
#trash
#server_encryption_options:
#    internode_encryption: none
#    keystore: conf/.keystore
#    keystore_password: cassandra
#    truststore: conf/.truststore
#    truststore_password: cassandra
"""

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
                #print(yaml.load(block.replace('#', '')))
                result.update(yaml.load(block.replace('#', '')))
                break
            except Exception as e:
                block_lines.pop()

    return result
