# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw


def is_higherequal(first: iamraw.Headline, second: iamraw.Headline):
    # TODO: Move to iamraw
    assert first
    if not second:
        return True
    if first.page > second.page:
        return True
    return first.end >= second.end
