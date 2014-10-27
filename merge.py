#!/usr/bin/env python

import sys
import re
from copy import deepcopy
from collections import OrderedDict
from optparse import OptionParser

try:
    import rtyaml as yaml
except ImportError:
    import yaml


def read_file(filename):
    try:
        f = open(filename, 'rb')
        l = f.read()
        f.close()
    except IOError as e:
        print("can't open file '" + filename + "'. aborting.")
        sys.exit(-1)
    else:
        return l

def merge(old, new, ask_user=False):
    try:
        old_dict = yaml.load(old) or {}
        new_dict = yaml.load(new) or {}
    except Exception as e:
        print('Cannot parse yaml')
        sys.exit(-1)

    merged = OrderedDict()
    for key, value in new_dict.items():
        old_value = old_dict.get(key)
        if old_value is not None:
            if ask_user:
                value = _choose_value(key, old_value, value)
            else:
                value = old_value
        merged.update({key: value})

    return old, new, yaml.dump(merged)

def preserve_comments(old, new, merged):
    lines = new.splitlines()
    comments, key_comments = [], {}
    for line in lines:
        if re.match(r'\s*#', line):
            comments.append(line)
        elif ':' in line:
            key, value = line.split(':')
            key = key.strip()
            key_comments[key] = comments
            comments = []
        elif re.match(r'^\s*$', line):
            comments.append('')

    if len(comments) > 0:
        tail_comments = "\n" + "\n".join(comments)
    else:
        tail_comments = ""

    merged_lines = merged.splitlines()
    merged_commented_lines = []
    for line in merged_lines:
        if ':' in line:
            key, value = line.split(':')
            key = key.strip()
            comments = key_comments.get(key)
            if comments is not None and len(comments) > 0:
                merged_commented_lines = merged_commented_lines + comments
        merged_commented_lines.append(line)

    return old, new, "\n".join(merged_commented_lines) + tail_comments

def _choose_value(key, old_value, new_value):
    if type(old_value) == type(new_value):
        return old_value
    print("New key %s has type '%s', but old key has type '%s'" % (
        key,
        type(new_value).__name__,
        type(old_value).__name__,
    ))
    answer = ''
    while answer not in ('o', 'n'):
        answer = raw_input("Please select to use [o]ld or [n]ew value: ")
    results = {
        'o': old_value,
        'n': new_value,
    }
    return results[answer]


if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] old_yaml new_yaml")

    parser.add_option("-o", "--output", dest="filename",
                  help="file to write result", metavar="FILE")
    parser.add_option("-n", "--no-comments",
                      action="store_true",
                      default=False,
                      help="dont preserve comments")
    parser.add_option("-a", "--ask",
                      action="store_true",
                      default=False,
                      help="ask user promt for confusing values")
    (options, args) = parser.parse_args()

    try:
        old_yaml, new_yaml = args
    except ValueError as e:
        print("only two files are allowed")
        sys.exit(-1)

    old, new, merged = merge(read_file(old_yaml), read_file(new_yaml), ask_user=options.ask)

    if not options.no_comments:
        old, new, merged = preserve_comments(old, new, merged)

    if options.filename is not None:
        with open(options.filename, 'w') as f:
            f.write(merged)
    else:
        print(merged)
