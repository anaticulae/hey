# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila


def uniform_result(items) -> iamraw.PageContentLikelihoods:
    # List[Item, Selector]
    # likelihood = Selector / Item

    values = items.values()
    max_features = sum([feature for _, feature in values])
    if max_features == 0:
        # no potential feature in document
        return {page: 0.0 for page in items}

    result = {
        page: (feature / max_features) for page, (_, feature) in items.items()
    }
    # round to 2 digits
    result = {page: utila.roundme(item) for page, item in result.items()}
    return result
