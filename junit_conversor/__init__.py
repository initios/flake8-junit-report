import sys
import xml.etree.cElementTree as ET


def _parse(file_name):
    lines = tuple(open(file_name, 'r'))
    parsed = {}

    for line in lines:
        splitted = line.split(":", 3)

        # Skip invalid lines
        if len(splitted) == 4:
            error = {
                'file': splitted[0].strip(),
                'line': splitted[1].strip(),
                'col': splitted[2].strip(),
                'detail': splitted[3].strip(),
                'code': splitted[3].strip()[:4]
            }

            case_name = '{file}:{line}:{col}:'.format(file=error['file'], line=error['line'], col=error['col'])
            parsed[case_name] = error

    return dict(parsed)


def _convert(origin, destination):
    parsed = _parse(origin)

    testsuite = ET.Element("testsuite")
    testsuite.attrib["errors"] = str(len(parsed))
    testsuite.attrib["failures"] = "0"
    testsuite.attrib["name"] = "flake8"
    testsuite.attrib["tests"] = str(len(parsed)) or "1"
    testsuite.attrib["time"] = "1"

    for case_name, error in parsed.items():
        testcase = ET.SubElement(testsuite, "testcase", name=case_name)
        kargs = {
            "file": error['file'],
            "line": error['line'],
            "col": error['col'],
            "message": error['detail'],
            "type": "flake8 %s" % error['code']
        }

        text = "{0}:{1} {2}".format(error['line'], error['col'], error['detail'])

        ET.SubElement(testcase, "failure", **kargs).text = text

    tree = ET.ElementTree(testsuite)

    if (2, 6) == sys.version_info[:2]:  # py26
        tree.write(destination, encoding='utf-8')
    else:
        tree.write(destination, encoding='utf-8', xml_declaration=True)
