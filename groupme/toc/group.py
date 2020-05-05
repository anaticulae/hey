# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses

import texmex.numbers

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
        value = texmex.numbers.arabic(item.upper())
        return RomanLevel(value=value, raw=item)

    try:
        letter, _ = item.split('.', maxsplit=1)
        letter = letter.upper()
    except ValueError:
        # TODO: REMOVE THIS HACK AFTER FIXING LINEREGEX
        letter = item.replace('Anhang', '').replace(':', '').strip()

    if letter in ('A', 'B', 'C', 'D'):
        result = AppendixLevel(value=letter, character=letter, raw=item)
        return result

    assert 0, str(item)
