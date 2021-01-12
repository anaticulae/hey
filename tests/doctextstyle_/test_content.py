# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.path
import power

import doctextstyle.features.content


def test_content():
    path = groupme.path.border_leftright(power.link(power.MASTER116_PDF))
    content = doctextstyle.features.content.content(path)

    expected = [
        ((89.29, 89.3, 61.16, 102.59), 109),
        ((102.59, 61.16, 89.29, 39.26), 7),
    ]
    assert content == expected
