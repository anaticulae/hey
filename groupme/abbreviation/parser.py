# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import groupme.abbreviation
import groupme.abbreviation.geometry
import groupme.abbreviation.simple

STRATEGIES = [
    groupme.abbreviation.simple.SimpleAbbreviationParser,
    groupme.abbreviation.geometry.GeometryAbbreviationParser,
]


def parse(data: groupme.abbreviation.AbbreviationData,
         ) -> iamraw.AbbreviationResult:
    assert isinstance(data.normal, list), type(data)
    assert isinstance(data.oneline, list), type(data)

    parsed = [strategy(data).result() for strategy in STRATEGIES]

    judged = judge(parsed)
    return judged


def judge(results) -> iamraw.AbbreviationResult:
    simple = results[0]
    geometry = results[1]

    more_than_double_parsed = (len(geometry) * 2) < len(simple)
    if more_than_double_parsed:
        return simple
    return geometry
