import os
import xml.etree.cElementTree as ET


def _parse(file_name):
    lines = tuple(open(file_name, 'r'))
    parsed = []

    for line in lines:
        splitted = line.split(":")
        parsed.append({
            'file': splitted[0].strip(),
            'line': splitted[1].strip(),
            'col': splitted[2].strip(),
            'detail': splitted[3].strip(),
        })

    return parsed


def _convert(origin, destination, delete_origin=False):
    parsed = _parse(origin)

    if len(parsed) < 1:
        return

    testsuite = ET.Element("testsuite")
    testsuite.attrib["errors"] = str(len(parsed))
    testsuite.attrib["failures"] = "0"
    testsuite.attrib["name"] = "flake8 failures"
    testsuite.attrib["tests"] = str(len(parsed))
    testsuite.attrib["time"] = "1"

    for line in parsed:
        ET.SubElement(testsuite, "testcase", file=line['file'],
                      line=line['line'], col=line['col']).text = line['detail']

    tree = ET.ElementTree(testsuite)
    tree.write(destination, encoding='utf-8', xml_declaration=True)

    if delete_origin:
        try:
            os.remove(destination)
        except OSError:
            pass
