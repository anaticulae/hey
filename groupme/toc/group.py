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

import iamraw
import texmex.numbers
import utila

import groupme.toc


def group_bychapter(items: groupme.toc.TocLines):
    """Group by chapter."""
    # TODO: DONT KNOW WHY WE NEED THIS?
    assert isinstance(items, list), type(items)
    for item in items:
        assert isinstance(item, groupme.toc.TocLine), type(item)

    result = []
    collected = []
    for item in items:
        if item.level is None:
            if collected:
                result.append(collected)
                collected = []
            result.append([item])
            continue
        if collected and collected[-1].level[0] != item.level[0]:
            result.append(collected)
            collected = [item]
        else:
            collected.append(item)
    if collected:
        result.append(collected)
    return result


@dataclasses.dataclass
class Level:
    # TODO: MOVE TO IAMRAW
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
    """Determine level out of parsed level string.

    Examples:
      - IV Anhang
      - 4.1.1 Datenschicht
      - 5 Implementierung
      - None Literaturverzeichnis

    >>> level('A')
    AppendixLevel(value='A', raw='A', character='A')
    """
    # TODO: SUPPORT 1. Abbildung
    # TODO: SUPPORT 1. Abb.
    # In the current implementation there are valid cause of 'A' in Abb/
    # Abbildung, but this is not the correct Point.
    if item is None:
        return None

    number = numbered_level(item)
    if number is not None:
        return Level(value=number, raw=item)

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


def numbered_level(raw: str) -> int:
    """Convert number to raw level.

    >>> numbered_level('5 Geology')
    1
    >>> numbered_level('2. Zentrum')
    1
    >>> numbered_level('2.1.3. Abschluss')
    3
    >>> numbered_level('2.1 Anhang')
    2
    >>> numbered_level('2..1... Fehlerfrei') # ignore typos
    2
    """
    # TODO: MOVE TESTS?
    raw = raw.strip()
    if not raw:
        return None
    raw = raw.split()[0]
    if not '.' in raw:
        return 1 if raw.isnumeric() else None
    # 2.1.3
    splitted = [item for item in raw.split('.') if item]
    return len(splitted)


def groupby_level(tableofcontent: groupme.toc.TocLines) -> iamraw.Toc:  # pylint:disable=R1260
    """Create `iamraw.Toc` out of list of `groupme.toc.TocLine

    Determine level of toc line and replace it with determined int-level.

    Args:
        tableofcontent: extracted table of content.
    Returns:
        Table of content with replaced levels.`
    """
    assert isinstance(tableofcontent, list), type(tableofcontent)

    def determine_level(level_) -> int:
        if level_ is None:
            return 1
        numbered = numbered_level(level_)
        if numbered is None:
            return 1
        return numbered

    outlines = []
    for line in tableofcontent:
        if not line:
            utila.error(f'problem while processing lines: {line}')
            continue
        if not isinstance(line, groupme.toc.TocLine):
            continue
        level_ = determine_level(line.level)
        section = iamraw.SectionRaw(
            level=level_,
            page=line.page,
            title=line.title,
            raw=line.raw,
            raw_location=line.raw_location,
        )
        outlines.append(section)

    def level_zero(items):
        """Ensure that no toc has level zero

        Problem:
            1 Einleitung
            1.1 Aufbau der Arbeit
            update every level to ensure
        """
        # TODO: REMOVE THIS?
        zero_level = min([item.level for item in items], default=utila.INF) == 0
        if zero_level:
            for item in items:
                item.level = item.level + 1
        return items

    outlines = level_zero(outlines)
    result = iamraw.create_toc(outlines)
    return result
