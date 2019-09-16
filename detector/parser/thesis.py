# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from collections import namedtuple
from re import search

import iamraw

from detector.parser import extract_match

# TODO: MOVE TO IAMRAW
TitleThesisType = namedtuple('TitleThesisType', 'typ, title raw')


def parse(token: str) -> TitleThesisType:
    collected = search(PATTERN, token)
    if not collected:
        return None

    # TODO: HOW TO HANDLE MULTIPLE COLLECTION, e.g. Master, Bachelor on the
    # same page.
    # TODO: ADD DIRECT IMPORT OF THESIS
    for item in iamraw.titlepage.THESIS:
        finding = collected[item.name]
        if not finding:
            continue
        raw = extract_match(collected)
        return TitleThesisType(item, finding, raw)
    assert 0, 'should not happen'
    return None


def construct_pattern():
    # TODO: REMOVE PATCH afer upgrading IAMRAW
    iamraw.titlepage.THESIS[iamraw.titlepage.DocumentType.MASTER].add(
        'Diplomarbeit',)
    pattern = []
    for key, values in iamraw.titlepage.THESIS.items():
        subpattern = []
        subpattern = '(?P<%s>(' % str(key.name)
        # reverse to have the longer pattern in front, `Masterarbeit` before
        # `Master`
        subpattern += ('|'.join(sorted(values, reverse=True)))
        subpattern += '))'
        pattern.append(subpattern)

    result = '(' + ('|'.join(pattern)) + ')'
    return result


PATTERN = construct_pattern()
