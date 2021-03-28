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

import doctextstyle.vector.cluster as dvc


def test_vector_cluster():
    source = power.link(power.HOME025_PDF)
    matrix, navis, fontstore = dvc.navigators(source)
    # (length, data)
    assert matrix.shape == (516, 4)
    clustered = dvc.clusterme(matrix, navis)
    result = dvc.decide(clustered, fontstore)
    assert result.text_family
    assert result.text_size == 11.96


def test_vector_headlines():
    source = power.link(power.HOME025_PDF)
    matrix, navis, fontstore = dvc.navigators(source)
    clustered = dvc.clusterme(matrix, navis)
    result = dvc.decide(clustered, fontstore)
    assert utila.near(result.h1_size, 24.78, diff=0.5)
    assert utila.near(result.h2_size, 17.22, diff=0.5)
    assert utila.near(result.h3_size, 14.35, diff=0.5)
