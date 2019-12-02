# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""toc - regex extractor
=====================

Extract headlines based on regex pattern.

design decision
---------------

Should we support following whitespaces?

    It is not required to support lines with ending whitespaces. Following
    whitespace puts water into the wine and leads to more missmatchings. The
    better approach is to improve the pdf-parser to avoid following
    whitespaces.

    See: :class:`tests.groupme_.toc.test_regex.test_extract_toc_line_whitespace_decission`.
"""

import contextlib
import re
import typing

import iamraw
import utila

import detector.parser
import groupme.toc
import groupme.toc.strategy as gts
import hey.text.regex as htr


class RegexTocExtractor(gts.ExtractorStrategy):

    def result(self) -> gts.ExtractionResult:
        pages = []
        for page in self.loaded.content:
            pages.append(utila.NEWLINE.join([item.text for item in page]))

        parsed = [parse(item) for item in pages]
        flat = utila.flatten(parsed)
        grouped = gts.group(flat)
        return grouped


def parse(content: str) -> groupme.toc.TocLines:
    """Parse table of content via regex.

    Args
        content(str): content of block of text
    Returns:
        ordered list form top to down of parse table of content
    Pattern:

        with level:

        .. code-block :: none

            X.      Chapter ........... 1
            X.X     Section . . . . . . 3

        or no level:

        .. code-block :: none

            Eidesstattliche Erklärung ........... 69
    """
    duplicated = content
    result = []
    for pattern in [
            EXTENDED_PATTERN,
            EXTENDED_PATTERN_LETTER,
            DICTONARY,
            NO_DOTS,
    ]:
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

    # remove duplications, which can occur when table of content is on the
    # same page.
    result = groupme.toc.remove_duplication(result)

    # Ensure that toc list is ordered by position on pdf page
    result = groupme.toc.sort_byposition(result, duplicated)
    return result


def parse_line(line):
    assert isinstance(line, str), type(line)
    for pattern in [
            EXTENDED_PATTERN,
            EXTENDED_PATTERN_LETTER,
            NO_DOTS,
            NO_LEVEL,
            DICTONARY,
    ]:
        matched = re.match(pattern, line)
        if matched:
            return extract_match(matched)
    return None


def parse_page(page: iamraw.Page) -> typing.List[groupme.toc.TocLine]:
    """Merge `page` to raw string and extract the lines of table of content.

    Hint:
        see `parse`
    """
    if isinstance(page, iamraw.Page):
        lines = utila.flatten([
            container for container in page
            if isinstance(container, iamraw.TextContainer)
        ])
        lines = [item.text for item in lines]
    else:
        # PageTextNavigator
        lines = [item.text for item in page]

    # collect lines with dots
    # lines = [item for item in lines if item.count('.') > 4]

    # strip lines
    lines = [item.strip() for item in lines]

    text = utila.NEWLINE.join(lines)

    # work
    result = parse(text)

    return result


LEVEL = r'(?P<level>(\d{1,2}\.)+\d{0,2})'
LEVEL_DOTTED_OPTIONAL = r'(?P<level>(\d{1,2}\.?)+\d{0,2})'

LEVEL_LETTER = r'(?P<level>(A|B|C|D)\.(\d{1,2}\.?)+\d{0,2})'

TEXT = (
    '(?P<text>'
    fr'{htr.UC_NWS}'  # ensure that text does not start with whitespace
    fr'{htr.UC_WS_NL}+?'
    fr'{htr.UC_NWS}+?'  # ensure that text does not end with whitespace
    ')')

WHITESPACES = r'[ ]{1,5}'
DOTTED = r'([ \.]{1,})'
PAGE = r'(?P<page>\d+)'

EXTENDED_PATTERN = re.compile(
    ('^'
     f'{LEVEL}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{DOTTED}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

EXTENDED_PATTERN_LETTER = re.compile(
    ('^'
     f'{LEVEL_LETTER}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{DOTTED}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

NO_DOTS = re.compile(
    ('^'
     f'{LEVEL_DOTTED_OPTIONAL}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{WHITESPACES}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.MULTILINE | re.UNICODE,
)

NO_LEVEL = re.compile(
    ('^'
     f'{TEXT}'
     f'{DOTTED}'
     f'{PAGE}'
     '$'),
    re.VERBOSE | re.UNICODE,
)

#  r'([ \.]{2,})'
LIST = [
    'A',
    'Abbildungsverzeichnis',
    'Anhang',
    'Bildquellen',
    'Glossar',
    'Internetquellen',
    'Listings',
    'Literatur',
    'Literaturverzeichnis',
    'Tabellenverzeichnis',
    r'Eidesstattliche\ Erklärung',
]

JOINED_LIST = '|'.join(LIST)

DICTONARY = re.compile(
    ('^'
     f'(?P<text>({JOINED_LIST}))'
     r'([ \.]{0,})'
     f'{PAGE}'),
    re.VERBOSE | re.UNICODE,
)


def extract_match(match: re.Match) -> groupme.toc.TocLine:
    assert isinstance(match, re.Match), type(match)
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
