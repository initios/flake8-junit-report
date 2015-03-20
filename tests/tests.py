import os
import unittest
import xml.dom.minidom

from click.testing import CliRunner
from junit_conversor import _parse, _convert
from junit_conversor.cli import conversion


current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.join(current_dir, os.pardir)
output_dir = os.path.join(current_dir, 'output')
example_files_dir = os.path.join(current_dir, 'flake8_example_results')
failed_flake8 = os.path.join(example_files_dir, 'failed_flake8.txt')
failed_flake8_with_invalid_lines = os.path.join(example_files_dir, 'failed_flake8_with_invalid_lines.txt')
valid_flake8 = os.path.join(example_files_dir, 'valid_flake8.txt')

junit_conversor_cli = os.path.join(current_dir, os.pardir, 'bin', 'junit_conversor')


class TestCase(unittest.TestCase):
    def assertXmlIsValid(self, xml_file):
        try:
            with open(xml_file) as f:
                content = f.read()

            xml.dom.minidom.parseString(content)
        except xml.parsers.expat.ExpatError:
            raise Exception('The specified file is not a valid XML (%s)'
                            % content[0:30])

    def assertFileExist(self, file_name):
        self.assertTrue(os.path.exists(file_name), 'File %s does not exist' % file_name)

    def assertFileDoesNotExist(self, file_name):
        self.assertFalse(os.path.exists(file_name), 'File %s exist' % file_name)


class ParseTest(TestCase):
    def test_should_parse_a_flake8_file_with_errors(self):
        parsed = _parse(failed_flake8)

        self.assertEqual(parsed, {
            "tests/subject/__init__.py": [
                {"file": "tests/subject/__init__.py", "line": "1", "col": "1", "detail": "F401 'os' imported but unused", "code": "F401"},
                {"file": "tests/subject/__init__.py", "line": "3", "col": "1", "detail": "E302 expected 2 blank lines, found 1", "code": "E302"},
            ],
            "tests/subject/example.py": [
                {"file": "tests/subject/example.py", "line": "4", "col": "1", "detail": "E302 expected 2 blank lines, found 1", "code": "E302"},
            ]
        })

    def test_should_return_an_empty_dict_when_parsing_a_flake8_success_file(self):
        self.assertEqual({}, _parse(valid_flake8))

    def test_should_skip_invalid_lines(self):
        parsed = _parse(failed_flake8_with_invalid_lines)

        self.assertEqual(parsed, {
            "tests/subject/__init__.py": [
                {"file": "tests/subject/__init__.py", "line": "1", "col": "1", "detail": "F401 'os' imported but unused", "code": "F401"},
                {"file": "tests/subject/__init__.py", "line": "3", "col": "1", "detail": "E302 expected 2 blank lines, found 1", "code": "E302"},
            ],
            "tests/subject/example.py": [
                {"file": "tests/subject/example.py", "line": "4", "col": "1", "detail": "E302 expected 2 blank lines, found 1", "code": "E302"},
            ]
        })


class ConvertTest(TestCase):
    def setUp(self):
        self.destination = os.path.join(output_dir, 'junit.xml')

        try:
            os.remove(self.destination)
        except OSError:
            pass

    def test_should_convert_a_file_with_flake8_errors_to_junit_xml(self):
        _convert(failed_flake8, self.destination)

        self.assertFileExist(self.destination)
        self.assertXmlIsValid(self.destination)

    def test_should_not_create_a_file_if_there_are_no_errors(self):
        _convert(valid_flake8, self.destination)
        self.assertFileDoesNotExist(self.destination)


class JunitConversorCliTest(TestCase):
    runner = CliRunner()

    def test_should_fail_if_source_file_is_not_given(self):
        result = self.runner.invoke(conversion, [])

        self.assertEqual(2, result.exit_code)
        self.assertIn('Missing argument "source"', result.output)

    def test_should_fail_if_destination_file_is_not_given(self):
        result = self.runner.invoke(conversion, [failed_flake8])

        self.assertEqual(2, result.exit_code)
        self.assertIn('Missing argument "destination', result.output)

    def test_should_make_a_simple_conversion(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(conversion, [failed_flake8, 'result.xml'])

            self.assertEqual(0, result.exit_code)
            self.assertEqual('Conversion done\n', result.output)
            self.assertFileExist('result.xml')
            self.assertXmlIsValid('result.xml')
