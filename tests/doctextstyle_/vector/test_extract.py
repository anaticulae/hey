# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import doctextstyle.vector.extract
import doctextstyle.vector.prepare


def test_vector_diss266_extract():
    source = power.link(power.DISS266_PDF)
    matrix, navis, _ = doctextstyle.vector.prepare.navigators(
        source,
        pages=utila.ranged_tuple(7, 200),
    )
    clustered = doctextstyle.vector.prepare.clusterme(matrix, navis)
    result = doctextstyle.vector.extract.extract_headlines(clustered)
    assert len(result) == 4
