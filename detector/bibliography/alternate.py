# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import texmex
import utila

import detector.bibliography.data
import hey.geometry.alternate


def extracts(items: texmex.PageTextNavigators,
            ) -> detector.bibliography.data.BibliographyReferences:
    result = []
    for item in items:
        extracted = extract(item)
        if not extracted:
            continue
        result.extend(extracted)
    return result


def extract(content: texmex.PageTextNavigator,
           ) -> detector.bibliography.data.BibliographyReferences:
    parsed = hey.geometry.alternate.parse_page(content)
    if parsed is None:
        return None
    result = []
    for group in parsed:
        raw = connect_text([item.text for item in group])
        reference, data = split_bibliography(raw)
        result.append(
            detector.bibliography.data.BibliographyReference(
                reference=reference,
                data=data,
            ))
    return result


# [HELM87]
PREFIX = r'^\[(?P<label>[\w\d]+)\][ ]?(?P<text>.+)'


def split_bibliography(raw: str):
    raw = raw.strip()
    reference, data = None, None

    matched = re.match(PREFIX, raw)
    if matched:
        return matched['label'], matched['text']

    reference, data = raw.split(maxsplit=1)
    return reference, data


def connect_text(items) -> str:
    items = [item.replace(utila.NEWLINE, ' ').strip() for item in items]
    # replace trennung
    items = [
        item[0:-1] if item[-1] in ('-', chr(173)) else item for item in items
    ]
    raw = ''.join(items)
    raw = raw.replace(utila.NEWLINE, ' ')
    return raw
