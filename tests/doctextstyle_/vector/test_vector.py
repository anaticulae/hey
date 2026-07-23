# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilo
import utilotest

import doctextstyle.vector.decide
import doctextstyle.vector.extract
import doctextstyle.vector.prepare as dvp


@utilotest.requires(hoverpower.HOME025_PDF)
def test_vector_cluster():
    source = hoverpower.link(hoverpower.HOME025_PDF)
    matrix, navis, fontstore = dvp.create_matrix(source)
    # (length, data)
    # the length varies by excluding some lines or different image/figure
    # extraction
    assert utilo.near(matrix.shape[0], 500, diff=30)
    assert matrix.shape[1] == 5
    clustered = dvp.clusterme(matrix, navis)
    result = doctextstyle.vector.decide.decide(
        clustered,
        fontstore,
        pagecount=len(navis),
    )
    assert result.text_family
    assert result.text_size == 11.96


@utilotest.requires(hoverpower.HOME025_PDF)
def test_vector_headlines():
    source = hoverpower.link(hoverpower.HOME025_PDF)
    # exclude title page from headline detection.
    # TODO: DECIDE TO EXCLUDE NON MAINPART SECTIONS?
    matrix, navis, fontstore = dvp.create_matrix(
        source,
        pages=utilo.rtuple(1, 25),
    )
    clustered = dvp.clusterme(matrix, navis)
    result = doctextstyle.vector.decide.decide(
        clustered,
        fontstore,
        pagecount=len(navis),
    )
    assert utilo.near(result.h1_size, 24.78, diff=0.5)
    assert utilo.near(result.h2_size, 17.22, diff=0.5)
    assert utilo.near(result.h3_size, 14.35, diff=0.5)
    assert result.h1_family == 'CMSSBX10'
    assert result.h2_family == 'CMSSBX10'
    # assert result.h3_family == 'CMSSBX10'
    assert result.h3_family in {'URWPalladioL', 'CMSSBX10'}
