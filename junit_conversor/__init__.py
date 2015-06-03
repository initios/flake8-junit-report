import xml.etree.cElementTree as ET
import os
import sys
from collections import defaultdict
import click


def _prepare_file_tree(path):
    tree = defaultdict(list)

    if not os.path.exists(path):
        click.echo('Given file path does not exists. Using only files '
                   'with errors from flake8 output.', err=True)
        return tree

    for (directory, _, files) in os.walk(path):
        for f in files:
            if f.endswith('.py'):
                tree[os.path.join(directory, f)] = []

    return tree


def _parse(file_name, all_files_path=False):
    lines = tuple(open(file_name, 'r'))
    parsed = defaultdict(list)

    if all_files_path:
        parsed = _prepare_file_tree(all_files_path)

    for line in lines:
        splitted = line.split(":")

        # Skip invalid lines
        if len(splitted) == 4:
            error = {
                'file': splitted[0].strip(),
                'line': splitted[1].strip(),
                'col': splitted[2].strip(),
                'detail': splitted[3].strip(),
                'code': splitted[3].strip()[:4]
            }

            parsed[error['file']].append(error)

    return dict(parsed)


def _convert(origin, destination, allways_create=False, all_files_path=False):
    parsed = _parse(origin, all_files_path=all_files_path)

    if len(parsed) < 1 and not allways_create:
        return

    testsuite = ET.Element("testsuite")
    testsuite.attrib["errors"] = str(len(parsed))
    testsuite.attrib["failures"] = "0"
    testsuite.attrib["name"] = "flake8 failures"
    testsuite.attrib["tests"] = str(len(parsed))
    testsuite.attrib["time"] = "1"

    for file_name, errors in parsed.items():
        testcase = ET.SubElement(testsuite, "testcase", name=file_name)

        for error in errors:
            ET.SubElement(testcase, "failure", file=error['file'], line=error['line'], col=error['col'],
                          message=error['detail'], type="flake8 %s" % error['code']) \
                          .text = "{0}:{1} {2}".format(error['line'], error['col'], error['detail'])

    tree = ET.ElementTree(testsuite)
    if (2, 6) == sys.version_info[:2]:  # py26
        tree.write(destination, encoding='utf-8')
    else:
        tree.write(destination, encoding='utf-8', xml_declaration=True)

