import xml.etree.cElementTree as ET
from collections import defaultdict


def _parse(file_name):
    parsed = defaultdict(list)

    with open(file_name, 'rb') as f:
        for line in f:
            line = line.decode("utf-8")
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


def _convert(origin, destination):
    parsed = _parse(origin)

    if len(parsed) < 1:
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
                          .text = "{}:{} {}".format(error['line'], error['col'], error['detail'])

    tree = ET.ElementTree(testsuite)
    tree.write(destination, encoding='utf-8', xml_declaration=True)
