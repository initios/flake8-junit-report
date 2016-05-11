import sys

from . import _convert


def main():
    flake8_file, destination_file = sys.argv[1:]
    _convert(flake8_file, destination_file)
    sys.stdout.write("File %s was created successfully" % destination_file)
    sys.exit(0)


if __name__ == "__main__":
    main()
