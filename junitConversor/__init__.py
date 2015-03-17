def _parse(file):
    lines = tuple(open(file, 'r'))
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
    pass
