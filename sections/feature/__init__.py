# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
# TODO: MOVE TO UTILA
import typing

import iamraw
import texmex
import utila

Count = int
Page = int
StatisticalResultItem = typing.Tuple[texmex.Occurrence, Count]  # number
StatisticalResult = typing.Dict[Page, StatisticalResultItem]


def uniform_result(items: StatisticalResult) -> iamraw.PageContentLikelihoods:
    assert isinstance(items, dict), type(items)
    values = items.values()
    max_features = sum([feature for _, feature in values])
    if not max_features:
        # no potential feature in document
        return {page: 0.0 for page in items}

    result = {
        page: (feature / max_features) for page, (_, feature) in items.items()
    }
    # round to 2 digits
    result = {page: utila.roundme(item) for page, item in result.items()}
    return result
