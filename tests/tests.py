import mock
import os
import unittest
import xml.dom.minidom

from junit_conversor import _parse, _convert


current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(current_dir, 'output')
example_files_dir = os.path.join(current_dir, 'flake8_example_results')
failed_flake8 = os.path.join(example_files_dir, 'failed_flake8.txt')
failed_flake8_with_invalid_lines = os.path.join(example_files_dir, 'failed_flake8_with_invalid_lines.txt')
valid_flake8 = os.path.join(example_files_dir, 'valid_flake8.txt')


class ParseTest(unittest.TestCase):
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


class ConvertTest(unittest.TestCase):
    def setUp(self):
        self.destination = os.path.join(output_dir, 'junit.xml')

        try:
            os.remove(self.destination)
        except OSError:
            pass

    def assertXmlIsValid(self, xml_file):
        try:
            with open(xml_file) as f:
                content = f.read()

            xml.dom.minidom.parseString(content)
        except xml.parsers.expat.ExpatError:
            raise Exception('The specified file is not a valid XML (%s)'
                % content[0:30])

    def test_should_convert_a_file_with_flake8_errors_to_junit_xml(self):
        _convert(failed_flake8, self.destination)

        self.assertTrue(os.path.exists(self.destination), 'The xml file should exist')
        self.assertXmlIsValid(self.destination)

    def test_should_not_create_a_file_if_there_are_no_errors(self):
        _convert(valid_flake8, self.destination)
        self.assertFalse(os.path.exists(self.destination), 'The xml file should not exist')


class JunitConversorTest(unittest.TestCase):
    @mock.patch('junit_conversor._parse')
    @mock.patch('junit_conversor._convert')
    def test_should_make_a_simple_conversion(self, _convert, _parse):
        self.assertTrue(_convert.called, '_convert was not called')
        self.assertTrue(_parse.called, '_parse was not called')
