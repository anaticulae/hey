# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.abbreviation
import groupme.abbreviation.geometry
import groupme.abbreviation.simple

STRATEGIES = [
    groupme.abbreviation.simple.SimpleAbbreviationParser,
    groupme.abbreviation.geometry.GeometryAbbreviationParser,
]


def parse(data: groupme.abbreviation.AbbreviationData,
         ) -> groupme.abbreviation.AbbreviationResult:
    assert isinstance(data.normal, list), type(data)
    assert isinstance(data.oneline, list), type(data)

    parsed = [strategy(data).result() for strategy in STRATEGIES]

    judged = judge(parsed)
    return judged


def judge(results) -> groupme.abbreviation.AbbreviationData:
    results = sorted(results, key=len, reverse=True)

    master = results[0]
    result = groupme.abbreviation.AbbreviationResult(master)
    return result
