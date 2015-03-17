import os
import unittest

from junitConversor import _parse


current_dir = os.path.dirname(os.path.realpath(__file__))
example_files_dir = os.path.join(current_dir, 'flake8_example_results')
failed_flake8 = os.path.join(example_files_dir, 'failed_flake8.txt')
valid_flake8 = os.path.join(example_files_dir, 'valid_flake8.txt')


class ParseTest(unittest.TestCase):
    def test_can_parse_a_flake8_file(self):
        parsed = _parse(failed_flake8)

        self.assertEqual(parsed, [
            {'file': 'tests/subject/__init__.py', 'line': '1', 'col': '1', 'detail': "F401 'os' imported but unused"},
            {'file': 'tests/subject/__init__.py', 'line': '3', 'col': '1', 'detail': "E302 expected 2 blank lines, found 1"},
            {'file': 'tests/subject/example.py', 'line': '4', 'col': '1', 'detail': "E302 expected 2 blank lines, found 1"},
        ])

    def test_parsing_an_flake8_success_file_returns_an_empty_list(self):
        self.assertEqual([], _parse(valid_flake8))
