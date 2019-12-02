# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses

import groupme.toc


def group(items: groupme.toc.TocLines):
    # TODO: RENAME GROUPBY_LEVEL
    assert isinstance(items, list), type(items)
    for item in items:
        assert isinstance(item, groupme.toc.TocLine), type(item)

    result = []

    current = None
    collected = []
    for item in items:
        level_ = level(item.level)
        if level_ is None or level_ != current:
            if collected:
                result.append(collected)
                collected = []
            current = level_
            collected.append(item)
        else:
            collected.append(item)
    if collected:
        result.append(collected)
    return result


def isascending(items):
    # TODO: MOVE TO UTILA
    items = [int(item) for item in items]
    diff = [
        (after - current) for (current, after) in zip(items[:-1], items[1:])
    ]
    return all([item >= 0 for item in diff])


@dataclasses.dataclass
class Level:
    value: int = None
    raw: str = dataclasses.field(compare=False, default=None)

    def __int__(self):
        return self.value


class RomanLevel(Level):
    pass


@dataclasses.dataclass
class AppendixLevel(Level):
    character: str = None
    """
    Example::
        A.1.1
    """

    def __int__(self):
        return 100  # HOLY VALUE


def level(item: str) -> Level:
    """

    Examples:
      - IV Anhang
      - 4.1.1 Datenschicht
      - 5 Implementierung
      - None Literaturverzeichnis
    """
    if item is None:
        return None

    with contextlib.suppress(ValueError):
        value = int(item)
        return Level(value=value, raw=item)

    with contextlib.suppress(ValueError):
        value = int(item.split('.')[0])
        return Level(value=value, raw=item)

    with contextlib.suppress(KeyError):
        value = ROMAN[item.upper()]
        return RomanLevel(value=value, raw=item)

    letter, _ = item.split('.', maxsplit=1)
    letter = letter.upper()

    if letter in ('A', 'B', 'C', 'D'):
        result = AppendixLevel(value=letter, character=letter, raw=item)
        return result

    assert 0, str(item)


#TODO: REPLACE WITH PYTHON PACKAGE WHICH SUPPORTS ROMAN NUMBERS
ROMAN = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IIII': 4,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
}
