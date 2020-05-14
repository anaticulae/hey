# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import tests.resources
import textstyle.cluster.page
import textstyle.parse.page


@pytest.fixture
def master116_text_flat():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.MASTER72,
        prefix='oneline',
        pages=tuple(range(3, 65)),
    )
    parsed = textstyle.parse.page.parses(navigators)
    flat = textstyle.cluster.page.flatten(parsed)
    return flat


def test_cluster_size(master116_text_flat):  # pylint:disable=W0621
    data = master116_text_flat
    selection = (textstyle.cluster.page.ClusterProperty.SIZE,)
    clustered = textstyle.cluster.page.cluster(data, selection=selection)
    assert len(master116_text_flat) >= 2000
    # six different font size cluster
    assert len(clustered) == 6
