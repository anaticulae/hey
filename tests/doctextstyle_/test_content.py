# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import utila
import utilatest

import doctextstyle.features.content


@utilatest.requires(power.MASTER116_PDF)
def test_content():
    source = power.link(power.MASTER116_PDF)
    path = iamraw.path.groupme_border_leftright(source)
    content = doctextstyle.features.content.content(path)
    expected = [
        ((89.29, 89.3, 65.71, 102.59), 109),
        ((102.59, 65.71, 89.29, 39.26), 7),
    ]
    for current, expect in zip(content, expected):
        assert current[1] == expect[1]
        assert utila.nears(current[0], expect[0], diff=0.5)
