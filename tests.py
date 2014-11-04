import unittest

from merge import merge, read_file, preserve_comments
from yaml_parser_extended import load_from_comments
import rtyaml as yaml

def get_data(folder):
    result = []
    for name in ['old.yaml', 'new.yaml', 'result.yaml']:
        result.append(read_file('fixtures/%s/%s' % (folder, name, )))
    return result

class TestMerge(unittest.TestCase):
    def _compare_fixtures(self, folder):
        old_yaml, new_yaml, result_yaml = get_data(folder)
        _, _, merged_yaml = merge(old_yaml, new_yaml)
        self.assertEqual(yaml.load(merged_yaml), yaml.load(result_yaml))

    def test_empty_files(self):
        self._compare_fixtures('empty')

    def test_old_empty(self):
        self._compare_fixtures('old_empty')

    def test_new_empty(self):
        self._compare_fixtures('new_empty')

    def test_full_rewrite(self):
        self._compare_fixtures('full_rewrite')

    def test_partly_rewrite(self):
        self._compare_fixtures('partly_rewrite')

    def test_complex_merge(self):
        self._compare_fixtures('complex_merge')

    def test_preserves_keys_order(self):
        self._compare_fixtures('keys_order')

    def test_commented_lines(self):
        self._compare_fixtures('commented_lines')


class TestPreserveComments(unittest.TestCase):
    def _compare(self, folder):
        old_yaml, new_yaml, result_yaml = get_data(folder)
        old_yaml, new_yaml, merged_yaml = merge(old_yaml, new_yaml)
        _, _, merged_with_comments = preserve_comments(old_yaml, new_yaml, merged_yaml)
        self.assertEqual(merged_with_comments.strip(), result_yaml.strip())

    def test_no_comments(self):
        self._compare('no_comments')

    def test_middle_comments(self):
        self._compare('middle_comments')

    def test_multiline_comments(self):
        self._compare('multiline_comments')

    def test_whiteline_comments(self):
        self._compare('whiteline_comments')

    def test_multiline_shifted_comments(self):
        self._compare('multiline_shifted_comments')

    def test_end_comments(self):
        self._compare('end_comments')


class TestExtendedParser(unittest.TestCase):
    def _get_comments_data(self, name):
        return load_from_comments(read_file('fixtures/%s/%s.yaml' % (name, name, )))

    def test_empty_comments(self):
        data = self._get_comments_data('empty_comments')
        self.assertEqual(data, {})

    def test_simple_line(self):
        data = self._get_comments_data('parser_simple')
        self.assertEqual(data, {'test3': 'asdasdsd'})

    def test_multiline(self):
        data = self._get_comments_data('parser_multiline')
        self.assertEqual(data.keys(), ['server_encryption_options'])

    def test_multiline_dirty(self):
        data = self._get_comments_data('parser_multiline_dirty')
        self.assertEqual(data.keys(), ['server_encryption_options'])


if __name__ == '__main__':
    unittest.main()
