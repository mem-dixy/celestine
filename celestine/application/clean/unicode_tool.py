"""
This is a modified main file, so might not run as application.

Converts the Unicode text file into a python dictionary.
Was run from the project root.
"""

import io

from celestine import (
    load,
    stream,
)
from celestine.typed import (
    GS,
    S,
)


def work(document: S) -> GS:
    for line in document:
        strip = line.strip()
        split = strip.split(";")

        number = split[0]
        number = int(number, 16)

        name = split[1]
        if name == "<control>":
            name = split[10]
            if name == "":
                # U+0099
                name = "Single Graphic Character Introducer"

        elif name[0] == "<":
            continue

        name = name.split("(")[0]
        name = name.strip()

        name = name.replace(" ", "_")
        name = name.replace("-", "_")

        text = f"{name} = chr({number})\n"

        yield text

        # TODO check indent of stuff below

        file = load.pathway("UnicodeData.txt")

        def read_stream(lines: GS) -> S:
            string = io.StringIO()
            for line in lines:
                string.write(line)

            value = string.getvalue()
            return value

        with stream.text.reader(file) as lines:
            loaded = read_stream(lines)
            text = work(loaded)
        stream.module.save(text, "unicode")
