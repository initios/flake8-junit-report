import os
import unittest


current_dir = os.path.dirname(os.path.realpath(__file__))
example_files_dir = os.path.join(current_dir, 'flake8_example_results')
failed_flake8 = os.path.join(example_files_dir, 'failed_flake8.txt')


class ConversorTest(unittest.TestCase):
    def test_converts_a_flake8_file_to_junit(self):
        assert True
