# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import re

import texmex

import detector.bibliography.data as dbd
import hey.geometry.alternate
import hey.text.utils

MIN_CONTENT_LENGTH = 15  # TODO: HOLY VALUE

MIN_WORD_COUNT = 2  # TODO: HOLY VALUE


def extracts(items: texmex.PageTextNavigators) -> dbd.BibliographyReferences:
    result = []
    config = hey.geometry.alternate.ParserConfig(
        min_content_length=MIN_CONTENT_LENGTH,
        min_word_count=MIN_WORD_COUNT,
    )
    try:
        parsed = hey.geometry.alternate.parse_pages(items, config=config)
    except hey.geometry.alternate.NoMultipleLiningPoints:
        return []
    for page in parsed:
        extracted = extract(page)
        result.append(extracted)
    return result


def extract(content) -> dbd.BibliographyReferences:
    if content is None:
        # white page
        return []
    result = []
    for group in content:
        raw = hey.text.utils.connect_text(group)
        reference, data = split_bibliography(raw)
        result.append(dbd.BibliographyReference(reference=reference, data=data))
    return result


# [HELM87]
PREFIX = r'^\[(?P<label>[\w\d]+)\][ ]?(?P<text>.+)'


def split_bibliography(raw: str):
    raw = raw.strip()
    reference, data = None, raw

    matched = re.match(PREFIX, raw)
    if matched:
        return matched['label'], matched['text']

    reference, data = authordate_pattern(raw)
    if reference:
        return reference, data

    with contextlib.suppress(ValueError):
        reference, data = raw.split(maxsplit=1)
    return reference, data


def authordate_pattern(raw: str):
    # TODO: SUPPORT HIGHNOTES
    """Split author and date, separated with colon from further bib data.

    >>> authordate_pattern('KUNCZIK, Michael/ZIPFEL, Astrid (52006): Gewalt'
    ... ' und Medien. Ein Studienhandbuch. Köln [u.a.]: Böhlau.')
    ('KUNCZIK, Michael/ZIPFEL, Astrid (52006)', 'Gewalt und Medien. ...
    """
    reference, data = None, raw
    with contextlib.suppress(ValueError):
        reference, data = raw.split(':', maxsplit=1)
    if reference:
        reference = reference.strip()
    data = data.strip()
    return reference, data
