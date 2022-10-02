import os
import unittest

from junit_conversor import _parse


current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.join(current_dir, os.pardir)
output_dir = os.path.join(current_dir, "output")
example_files_dir = os.path.join(current_dir, "flake8_example_results")
failed_flake8 = os.path.join(example_files_dir, "failed_flake8.txt")
failed_flake8_with_invalid_lines = os.path.join(example_files_dir, "failed_flake8_with_invalid_lines.txt")
valid_flake8 = os.path.join(example_files_dir, "valid_flake8.txt")

junit_conversor_cli = os.path.join(current_dir, os.pardir, "bin", "junit_conversor")


def test_should_parse_a_flake8_file_with_errors():
    parsed = _parse(failed_flake8)
    expected = {
        "tests/subject/__init__.py": [
            {
                "file": "tests/subject/__init__.py",
                "line": "1",
                "col": "1",
                "detail": "F401 'os' imported but unused",
                "code": "F401",
            },
            {
                "file": "tests/subject/__init__.py",
                "line": "3",
                "col": "1",
                "detail": "E302 expected 2 blank lines, found 1",
                "code": "E302",
            },
        ],
        "tests/subject/example.py": [
            {
                "file": "tests/subject/example.py",
                "line": "4",
                "col": "1",
                "detail": "E302 expected 2 blank lines, found 1",
                "code": "E302",
            },
            {
                "file": "tests/subject/example.py",
                "line": "16",
                "col": "22",
                "detail": "E203 whitespace before ':'",
                "code": "E203",
            },
        ],
    }
    assert parsed == expected


def test_should_return_an_empty_dict_when_parsing_a_flake8_success_file():
    assert _parse(valid_flake8) == {}


def test_should_skip_invalid_lines():
    parsed = _parse(failed_flake8_with_invalid_lines)

    expected = {
        "tests/subject/__init__.py": [
            {
                "file": "tests/subject/__init__.py",
                "line": "1",
                "col": "1",
                "detail": "F401 'os' imported but unused",
                "code": "F401",
            },
            {
                "file": "tests/subject/__init__.py",
                "line": "3",
                "col": "1",
                "detail": "E302 expected 2 blank lines, found 1",
                "code": "E302",
            },
        ],
        "tests/subject/example.py": [
            {
                "file": "tests/subject/example.py",
                "line": "4",
                "col": "1",
                "detail": "E302 expected 2 blank lines, found 1",
                "code": "E302",
            },
        ],
    }
    assert parsed == expected
