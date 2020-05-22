# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import doctextstyle.features.content
import groupme.path
import tests.resources


def test_content():
    path = groupme.path.border_leftright(tests.resources.MASTER116)
    content = doctextstyle.features.content.content(path)

    expected = [
        ((89.29, 505.98, 61.16, 739.3), 109),
        ((89.29, 505.98, 89.29, 556.02), 7),
    ]
    assert content == expected
