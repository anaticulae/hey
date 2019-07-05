# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

NDIGITS = 2


def roundme(value: float):
    """Round value to `NDGITS`=2"""
    return round(value, NDIGITS)


def flatten(lists):
    result = []
    for item in lists:
        result.extend(item)
    return result
