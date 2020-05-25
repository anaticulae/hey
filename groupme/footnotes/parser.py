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

  - "1 Aus Gründen der besseren Lesbarkeit wird hier und im "

- bibliography:

  - "5 s. Berg 2013: 2"
  - "6 Gero von Randow, zeit.de, 19.1.2007"


.. todo::

  - TODO: FOR FURTHER ANALYSIS WE REQUIRE DIFFERENT FOOTER LINE ANALYZER


  ? we have to use a combination of font rise and maybe textual grammar ?
"""
import re

import iamraw
import utila

import groupme.footnotes.highnotes


def parse(content: str):
    assert isinstance(content, str), type(content)
    result = []

    for item in footnote_split(content):
        number, text = item.split(maxsplit=1)
        if not text.strip():
            utila.error(f'could not parse footnote: {number}, no text content')
            continue
        footnote = iamraw.FootRawNote(
            number=int(number),
            text=text,
            raw=item,
        )
        result.append(footnote)
    return result


def footnote_split(raw: str) -> list:
    """Split footnote into chunks. A empty newline or a starting
    footnote([int, whitespace]) marks the ending of a multiline footnote.

    Example:
    .. code-block:: none

        ...End of some Text.

        1 I am the first note
        2 I am a
        very long
        multiline note.

        I am a lonely newline which will not pass.
        3 But i will pass the test

        30 Helm

        Start of some text..
    """
    pattern = r'^\d{1,4}[ ]{1,5}'
    result = []
    for item in raw.splitlines():
        item = item.strip()
        if not item:
            # empty newline separates list elements from text
            result.append(None)
        if re.match(pattern, item):
            # match line start pattern
            result.append([item])
        else:
            if result and result[-1]:
                # ensure to have valid predecessor
                result[-1].append(item)
    joined = [' '.join(item) for item in result if item]
    return joined


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
            utila.info(f'footer - could not parse: "{item}"')
            continue
        footnotes.extend(parsed)
    return footnotes


def parse_with_highnotes(content):
    splitted = groupme.footnotes.highnotes.split_textinfo(content)
    merged = groupme.footnotes.highnotes.merge_online(splitted)
    result = []
    for number, note in merged:
        try:
            notenumber = int(number.text)
        except ValueError:
            utila.error(f'could not convert to int: {number.text}')
            notenumber = number.text
        if not note.text.strip():
            utila.error(f'could not parse footnote: {number}, no text content')
            continue

        footnote = iamraw.FootRawNote(
            number=notenumber,
            text=note.text,
            raw='',  # TODO: REMOVE THIS?
            style=(number.style, note.style),
        )
        result.append(footnote)
    return result
