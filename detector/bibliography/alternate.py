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
import utila

import detector.bibliography.data as dbd
import hey.geometry.alternate


def extracts(items: texmex.PageTextNavigators) -> dbd.BibliographyReferences:
    result = []
    for item in items:
        extracted = extract(item)
        if not extracted:
            continue
        result.extend(extracted)
    return result


def extract(content: texmex.PageTextNavigator,) -> dbd.BibliographyReferences:
    parsed = hey.geometry.alternate.parse_page(content)
    if parsed is None:
        return None
    result = []
    for group in parsed:
        raw = connect_text([item.text for item in group])
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

    with contextlib.suppress(ValueError):
        reference, data = raw.split(maxsplit=1)
    return reference, data
