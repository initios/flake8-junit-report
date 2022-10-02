import os
import pytest
import xml.dom.minidom

from junit_conversor import _convert

current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.join(current_dir, os.pardir)
output_dir = os.path.join(current_dir, "output")
example_files_dir = os.path.join(current_dir, "flake8_example_results")
failed_flake8 = os.path.join(example_files_dir, "failed_flake8.txt")
failed_flake8_with_invalid_lines = os.path.join(example_files_dir, "failed_flake8_with_invalid_lines.txt")
valid_flake8 = os.path.join(example_files_dir, "valid_flake8.txt")

junit_conversor_cli = os.path.join(current_dir, os.pardir, "bin", "junit_conversor")


def assertXmlIsValid(xml_file):
    try:
        with open(xml_file) as f:
            content = f.read()

        xml.dom.minidom.parseString(content)
    except xml.parsers.expat.ExpatError:
        raise Exception("The specified file is not a valid XML (%s)" % content[0:30])


def assertFileExist(file_name):
    assert os.path.exists(file_name), "File %s does not exist" % file_name


def assertFileDoesNotExist(file_name):
    assert os.path.exists(file_name) == False, "File %s exist" % file_name


@pytest.fixture
def result_file():
    destination = os.path.join(output_dir, "junit.xml")

    yield destination

    try:
        os.remove(destination)
    except OSError:
        pass


def test_should_convert_a_file_with_flake8_errors_to_junit_xml(result_file):
    _convert(failed_flake8, result_file)

    assertFileExist(result_file)
    assertXmlIsValid(result_file)


def test_should_create_a_file_even_when_there_are_no_errors(result_file):
    _convert(valid_flake8, result_file)
    assertFileExist(result_file)
