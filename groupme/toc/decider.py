# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""toc result extraction decider
=============================

The decision strategy is implemented as a `ExtractionStatistic`-comparer
implemented in `__lt__` method.
"""
import dataclasses

import utila

import groupme.toc.strategy as gts


@dataclasses.dataclass(unsafe_hash=True)
class ExtractionStatistic:
    validitem_count: int
    group_count: int
    oneline_factor: float

    def __lt__(self, item):
        # TODO: IMRPOVE THIS SIMPLE STRATEGY
        if self.validitem_count == item.validitem_count:
            return self.oneline_factor < item.oneline_factor
        return self.validitem_count > item.validitem_count


def decide(items: gts.ExtractionResults) -> gts.ExtractionResult:
    if not items:
        return None
    analyzed = [analyze_result(item) for item in items]
    selector = {result: item for result, item in zip(analyzed, items)}

    order = sorted(analyzed)
    first_item = order[0]
    selected = selector[first_item]
    return selected


def analyze_result(groups) -> ExtractionStatistic:
    if not groups:
        return None
    flat = utila.flatten(groups)

    oneliner = len([item for item in groups if len(item) == 1])
    oneline_factor = utila.roundme(oneliner / len(groups))

    return ExtractionStatistic(
        validitem_count=len(flat),
        group_count=len(groups),
        oneline_factor=oneline_factor,
    )
