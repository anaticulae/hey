# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import doctextstyle.cluster


def test_cluster_size(master72_text_flat):  # pylint:disable=W0621
    data = master72_text_flat
    selection = (doctextstyle.cluster.ClusterProperty.SIZE,)
    clustered = doctextstyle.cluster.cluster(
        data,
        selection=selection,
        max_size_diff=doctextstyle.cluster.Tol(0.0, 0.0),
    )
    assert len(master72_text_flat) >= 2000
    # six different font size cluster
    assert len(clustered) == 6
