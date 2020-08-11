# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
    invalid_count: int = 0
    parsed_level: int = 0

    def __lt__(self, item):
        # TODO: IMRPOVE THIS SIMPLE STRATEGY
        if self.invalid_count == item.invalid_count:
            if self.validitem_count == item.validitem_count:
                if self.parsed_level == item.parsed_level:
                    return self.oneline_factor < item.oneline_factor
                return self.parsed_level > item.parsed_level
            return self.validitem_count > item.validitem_count
        return self.invalid_count < item.invalid_count


def decide(items: gts.ExtractionResults) -> gts.ExtractionResult:
    if not items:
        return None
    analyzed = [analyze_result(item) for item in items]
    selector = {result: item for result, item in zip(analyzed, items)}
    order = sorted(analyzed)
    first_item = order[0]
    selected = selector[first_item]
    return selected


def analyze_result(result: gts.ExtractionResult) -> ExtractionStatistic:
    # TODO: REMOVE FLATTEN
    # TODO: REMOVE valid_content = groupme.toc.strategy.group(valid_content)
    flat = utila.flatten(result)
    oneliner = len([item for item in result if len(item) == 1])
    parsed_level = [item.level for item in flat if item.level is not None]
    oneline_factor = 0.0
    if len(result) >= 1:
        oneline_factor = utila.roundme(oneliner / len(result))  # pylint:disable=R0204

    result = ExtractionStatistic(
        validitem_count=len(flat),
        invalid_count=len(result.invalid),
        group_count=len(result),
        oneline_factor=oneline_factor,
        parsed_level=len(parsed_level),
    )
    return result
