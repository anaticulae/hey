# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.toc.decider
import groupme.toc.strategy
import groupme.toc.strategy.geometry
import groupme.toc.strategy.georegex
import groupme.toc.strategy.regex


def extract(
        data: groupme.toc.strategy.ExtractionData,
        active: list = None,
) -> groupme.toc.strategy.ExtractionResult:
    """Run various strategies to extract ``toc-lines`` out of given ``data``.

    Args:
        data: loaded data
        active: List of executed stratgies. Use ``None`` to run
                         all strategies.
    Returns:
        List of ``ExtractionResult`` with extracted data.
    """

    strategies = [
        groupme.toc.strategy.geometry.GeometryTocExtractor,
        groupme.toc.strategy.georegex.GeometryRegexTocExtractor,
        groupme.toc.strategy.regex.RegexTocExtractor,
    ]
    results = [
        strategy(data).result()
        for strategy in strategies
        # decide if strategy is active
        if active is None or strategy in active
    ]

    decision = groupme.toc.decider.decide(results)
    return decision
