# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import detector.bibliography.reference.tech
import hey.geometry.double_column


def extracts(items: texmex.PageTextNavigators):
    result = []
    for item in items:
        extracted = extract(item)
        if not extracted:
            continue
        result.append(extracted)
    return result


def extract(content: texmex.PageTextNavigator) -> iamraw.BibliographyReferences:
    parsed = hey.geometry.double_column.parse_page(content)
    if parsed is None:
        return None

    result = []
    for item in parsed:
        reference = item[0].strip()
        # remove latex reference pattern [FCB87]
        reference = remove_bracket_angle(reference)
        data = item[1].strip()

        techref = detector.bibliography.reference.tech.parse_longtext(data)
        if techref:
            techref.reference = reference
            techref.data = data
            result.append(techref)
        else:
            result.append(
                iamraw.BibliographyReference(
                    reference=reference,
                    data=data,
                ))
    return result


def remove_bracket_angle(reference: str):
    """Remove bracket angle at start and and of `reference`.

    >>> remove_bracket_angle('[TM12]')
    'TM12'
    >>> remove_bracket_angle('DSB')
    'DSB'
    """
    reference = reference.strip()
    if reference[0] == '[':
        reference = reference[1:]
    if reference[-1] == ']':
        reference = reference[0:-1]
    return reference
