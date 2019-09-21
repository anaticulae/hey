# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import re
import typing

import iamraw
import utila

import detector.parser
import groupme.toc
import hey


def parse(content: str) -> typing.List[groupme.toc.TocLine]:
    """Parse table of content via regex.

    Args
        content(str): content of block of text
    Returns:
        ordered list form top to down of parse table of content
    Pattern:
        X.      Chapter ........... 1
        X.X     Section . . . . . . 3

        no_level:
            Eidesstattliche Erklärung ........... 69
    """
    duplicated = content
    result = []
    for pattern in [EXTENDED_PATTERN, NO_DOTS]:
        for line in re.finditer(pattern, content):
            item = extract_match(line)
            result.append(item)
            # remove already match content to do not confuse lower strict
            # pattern
            content = content.replace(item.raw, '')

    # TODO: improve this
    for line in [item for item in content.splitlines() if item.strip()]:
        if re.match(r'^\d', line):
            continue
        matched = re.match(NO_LEVEL, line)
        if not matched:
            continue
        matched = extract_match(matched)
        result.append(matched)

    # remove duplications, which can occur when table of content is on the same page
    result = groupme.toc.remove_duplication(result)

    # Ensure that toc list os orderd by position on pdf page
    result = groupme.toc.sort_byposition(result, duplicated)
    return result


def parse_page(page: iamraw.Page) -> typing.List[groupme.toc.TocLine]:
    """Merge `page` to raw string and extract the lines of table of content.

    Hint:
        see `parse`
    """
    lines = utila.flatten([
        container for container in page
        if isinstance(container, iamraw.TextContainer)
    ])
    lines = [item.text for item in lines]

    # collect lines with dots
    # lines = [item for item in lines if item.count('.') > 4]

    # strip lines
    lines = [item.strip() for item in lines]

    text = utila.NEWLINE.join(lines)

    # work
    result = parse(text)

    return result


USER_CONTENT = r'\w\d\.&:, \-' + hey.utils.SPECIAL_MINUS_SIGN
WITH_NEWLINE = r'\s'

# \W to ensure non-unicode character, like special - chars
EXTENDED_PATTERN = re.compile(
    (r'^'
     r'(?P<level>(\d{1,2}\.)+\d{0,2})'
     r'[ ]{1,5}'
     fr'(?P<text>[{USER_CONTENT}{WITH_NEWLINE}]+?\w+?)'
     r'([ \.]{3,})'
     r'(?P<page>\d+)'
     r'$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

NO_DOTS = re.compile(
    (r'^'
     r'(?P<level>(\d))'
     r'[ ]{1,5}'
     r'(?P<text>[\w ]+)'
     r'$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

NO_LEVEL = re.compile(
    (r'^'
     fr'(?P<text>[{USER_CONTENT}]+?\w+?)'
     r'([ \.]{3,})'
     r'(?P<page>\d+)'),
    re.VERBOSE | re.UNICODE,
)


def extract_match(match) -> groupme.toc.TocLine:
    level, title, page = None, match['text'], None
    with contextlib.suppress(IndexError):
        page = match['page']
    with contextlib.suppress(IndexError):
        level = match['level']

    result = groupme.toc.TocLine(
        level=level,
        title=title,
        page=page,
        raw=detector.parser.extract_match(match),
    )
    return result
