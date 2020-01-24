# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module parses :class:`iamraw.FootNote` out of raw text data.

There are 2 supported types of footnotes:

- raw text:

  - "Aus Gründen der besseren Lesbarkeit wird hier und im "

- literature:

  - "s. Berg 2013: 2"
  - "Gero von Randow, zeit.de, 19.1.2007"


.. todo::

  - TODO: FOR FURTHER ANALYSIS WE REQUIRE DIFFERENT FOOTER LINE ANALYZER
  - TODO: SUPPORT MULTILINE FOOTNOTES

.. problem::

  using regex to extract footnotes is not enough. There can not be
  decided if a number is a footnote start or a normaly number in a
  footnote.

  we have to use a combination of font rise and maybe textual grammar.
"""
import re

import iamraw
import utila

import detector.parser
import groupme.footnotes.highnotes

# TODO: REPLACE WITH GENERAL TEXT PARSER
# TODO: ADD REGEX BIB TO `GET_TEXT_PATTERN(name='text')`
PATTERN = r"""
        ^
        (?P<number>\d{1,4}) # up to 4 digits foot-note-numbers
        [ ]{0,5} # whitespaces between number and foot note text
        (?P<text>[\w\d:\.,;’„“/\(\)\[\]\n \-]{5,}?) # more than 5 chars
        $"""
PATTERN = re.compile(PATTERN, re.VERBOSE)


def parse(content: str):
    assert isinstance(content, str), type(content)
    result = []
    parsed = re.finditer(PATTERN, content)
    for item in parsed:
        number = item['number']
        text = item['text']
        raw = detector.parser.extract_match(item)

        footnote = iamraw.FootRawNote(
            number=number,
            text=text,
            raw=raw,
        )
        result.append(footnote)
    return result


def count_empty(items: iamraw.PageContentFooterHeader) -> int:
    """Count `MovingFooterInformation` which contain a empty `notes` list"""
    footers = [item.footer for item in items if item.footer]
    empty_footnotes = [item for item in footers if len(item.notes) == 0]
    result = len(empty_footnotes)
    return result


def parse_footer(content):
    footnotes = []
    splitted = groupme.footnotes.highnotes.split(content)
    for item in splitted:
        parsed = parse(item)
        if not parsed:
            utila.info(f'could not parse: "{item}"')
            continue
        footnotes.extend(parsed)
    return footnotes


def parse_with_highnotes(content):
    splitted = groupme.footnotes.highnotes.split_textinfo(content)
    merged = groupme.footnotes.highnotes.merge_online(splitted)
    return merged
