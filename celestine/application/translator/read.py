"""Reads in python dictionary files."""

import io

from celestine import stream
from celestine.data.alphabet2 import UNICODE
from celestine.literal import (
    LINE_FEED,
    REVERSE_SOLIDUS,
)
from celestine.typed import (
    GS,
    S,
)


def fix_line_split(*path: S) -> GS:
    """"""
    skip = False

    document = stream.module.load(*path)
    for string in document:
        for character in string:
            if character not in UNICODE:
                continue

            if character == REVERSE_SOLIDUS:
                skip = True
                continue

            if skip:
                skip = False
                continue

            yield from character


def make_dictionary(document):
    """"""
    dictionary = {}

    lines = document.split(LINE_FEED)
    for line in lines:
        if line[0:3] == '"""':
            continue

        if not line:
            continue
        split = line.split("=")
        key = split[0].strip()
        value = split[-1].strip()[1:-1]
        dictionary[key] = value
    return dictionary


def open_language(*path):
    """Convert a dictionary to a string and save it to a file."""
    text = fix_line_split(*path)
    lines = read_new_lines(text)
    normal = lines

    string = io.StringIO()
    for line in normal:
        string.write(line)

    value = string.getvalue()

    split = value.split(stream.SECTION_BREAK)

    head = make_dictionary(split[0])
    body = make_dictionary(split[-1])

    return (head, body)


def read_new_lines(string: S) -> GS:
    """"""

    buffer = io.StringIO()
    count = 0

    for character in string:
        count += buffer.write(character)

        if character == LINE_FEED:
            buffer.seek(0, io.SEEK_SET)
            line = buffer.read(count)
            buffer.seek(0, io.SEEK_SET)
            count = 0
            yield from line
