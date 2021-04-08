# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import iamraw

Line = collections.namedtuple(
    'Line',
    'rate, upper, size, bold, italic, left, right, top, bottom',
)
Lines = typing.List[Line]


def run(source: str, pages: tuple = None) -> iamraw.DocTextStyle:
    import doctextstyle.vector.decide
    import doctextstyle.vector.prepare
    matrix, loaded, fontstore = doctextstyle.vector.prepare.create_matrix(
        source,
        pages,
    )
    clustered = doctextstyle.vector.prepare.clusterme(
        matrix,
        loaded,
    )
    result = doctextstyle.vector.decide.decide(
        clustered,
        fontstore,
    )
    return result
