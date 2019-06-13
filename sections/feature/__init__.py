# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import List


def uniform_result(items) -> List[float]:
    # List[Item, Selector]
    # likelihood = Selector / Item
    sum_lines = sum([toc_line for _, toc_line in items])
    if sum_lines == 0:
        # no potential toc in document
        return [0.0 for _ in items]
    result = [toc / sum_lines for (_, toc) in items]
    return result
