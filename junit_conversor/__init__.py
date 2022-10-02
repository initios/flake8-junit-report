import xml.etree.cElementTree as ET
import sys
from collections import defaultdict


def _parse(file_name):
    lines = tuple(open(file_name, "r"))
    parsed = defaultdict(list)

    for line in lines:
        splitted = line.split(":", 3)

        # Skip invalid lines
        if len(splitted) == 4:
            error = {
                "file": splitted[0].strip(),
                "line": splitted[1].strip(),
                "col": splitted[2].strip(),
                "detail": splitted[3].strip(),
                "code": splitted[3].strip()[:4],
            }

            parsed[error["file"]].append(error)

    return dict(parsed)


def _convert(origin, destination):
    parsed = _parse(origin)

    testsuite = ET.Element("testsuite")
    testsuite.attrib["errors"] = str(len(parsed))
    testsuite.attrib["failures"] = "0"
    testsuite.attrib["name"] = "flake8"
    testsuite.attrib["tests"] = str(len(parsed)) or "1"
    testsuite.attrib["time"] = "1"

    for file_name, errors in parsed.items():

        for error in errors:
            kargs_failure = {"file": file_name, "message": error["detail"], "type": "flake8 %s" % error["code"]}
            kargs_testcase = {
                "name": "{0}:{1} {2}".format(error["line"], error["col"], error["detail"]),
                "line": error["line"],
                "col": error["col"],
                "file": file_name,
            }

            testcase = ET.SubElement(testsuite, "testcase", **kargs_testcase)
            text = "{0} {1}:{2} {3}".format(file_name, error["line"], error["col"], error["detail"])
            ET.SubElement(testcase, "failure", **kargs_failure).text = text

    tree = ET.ElementTree(testsuite)
    tree.write(destination, encoding="utf-8", xml_declaration=True)
