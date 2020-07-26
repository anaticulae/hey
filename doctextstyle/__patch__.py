# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def pnear(
        reference,
        current,
        rel_tol: float = 0.0,
        abs_tol: float = 0.05,
) -> bool:
    """\
    >>> pnear(10, 8, 0.2)
    True
    >>> pnear(10, 8, 0.19)
    False
    >>> pnear(0, 0.1, rel_tol=0.02, abs_tol=0.1)
    True
    """
    # TODO: UNIT WITH NEAR?
    lower = reference * (1 - rel_tol)
    upper = reference * (1 + rel_tol)
    if lower <= current <= upper:
        return True
    lower = reference - abs_tol
    upper = reference + abs_tol
    if lower <= current <= upper:
        return True
    return False


utila.pnear = pnear
