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


def multiform_result(items):
    """Use local likelihood for multiple feature pages.

    Support multiple feature pages. If we have more than one feature
    page, for example a toc which is expanded over three pages, the
    relative likelihood for every page is splitted between these three
    pages. See `uniform_result`. Therefore we need a different approach.

    The following approach checks for multiple featurepages, if there is
    only one page `None` as error is returned and we can use
    `uniform_result` approach.
    If we have multiple pages we compute the local likelihood for every
    page and ignore pages which does not have at least the half of the
    findings as the master page.

    NOTE: BAD DOCS
    TODO: What should we do with small feature pages?
    """
    assert isinstance(items, dict), type(items)
    values = items.values()
    max_features = sum([feature for _, feature in values])
    if not max_features:
        # no potential feature in document
        return {page: 0.0 for page in items}

    max_per_page = max([feature for _, feature in values])
    max_half = 0.5 * max_per_page
    multi_max = [feature for _, feature in values if feature >= max_half]
    if len(multi_max) < 2:
        # not enough multi form elements
        return None
    result = {
        page: (feature / lines) if feature > max_half else 0.0
        for page, (lines, feature) in items.items()
    }
    # round to 2 digits
    result = {page: utila.roundme(item) for page, item in result.items()}
    return result
