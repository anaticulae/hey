# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import doctextstyle.vector


def test_fast():
    source = power.link(power.HOME025_PDF)
    matrix, navigators, fontstore = doctextstyle.vector.navigators(source)
    # (length, data)
    assert matrix.shape == (516, 4)
    clustered = doctextstyle.vector.clusterme(matrix, navigators)
    result = doctextstyle.vector.decide(clustered, fontstore)
    assert result.text_family
    assert result.text_size == 11.96
