# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import texmex
import utila

import detector.bibliography.reference.tech
import hey.geometry.alternate
import hey.text.utils

MIN_CONTENT_LENGTH = 15  # TODO: HOLY VALUE

MIN_WORD_COUNT = 2  # TODO: HOLY VALUE


def extracts(items: texmex.PageTextNavigators) -> iamraw.BibliographyReferences:
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


def extract(content) -> iamraw.BibliographyReferences:
    if content is None:
        # white page
        return []
    result = []
    for group in content:
        raw = hey.text.utils.connect_text(group)
        reference, data = split_bibliography(raw)
        result.append(
            iamraw.BibliographyReference(
                reference=reference,
                data=data,
            ))
    return result


def split_bibliography(raw: str):
    raw = raw.strip()
    reference, data = None, raw

    technical = technical_pattern(raw)
    if technical:
        return technical

    reference, data = authordate_pattern(raw)
    if reference:
        return reference, data

    with contextlib.suppress(ValueError):
        reference, data = raw.split(maxsplit=1)
    return reference, data


def technical_pattern(raw: str):
    matched = detector.bibliography.reference.tech.parses(raw)
    if not matched:
        return None
    if len(matched) >= 2:
        utila.error(f'more than one references detected: {raw}')
    matched = matched[0]
    data = raw.replace(matched.raw, '').strip()
    number = matched.number if matched.number else ''
    reference = f'{matched.reference}{matched.year}{number}'
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
