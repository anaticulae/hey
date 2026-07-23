# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilotest

import doctextstyle.features.headline


@pytest.mark.xfail(reason='do not support multiline headlines')
@utilotest.longrun
def test_cluster_extract_headlines_small(master72_text_flat_small):
    # TODO: REQUIRE MULTILINE SUPPORT
    # TODO: SEE HEADLINE ON PAGE 6(FIRST LEVEL HEADLINES)
    headlines = doctextstyle.features.headline.headlines(
        master72_text_flat_small,
        min_headline_count=3,
        headline_start=True,
        returncluster=True,
    )
    assert len(headlines) == 2
    assert headlines[0][0] == 15.96
    assert headlines[1][0] == 14.04


@pytest.mark.xfail(reason='do not support multiline headlines')
@utilotest.longrun
def test_cluster_extract_headlines_all(master72_text_flat):
    # TODO: REQUIRE MULTILINE SUPPORT
    headlines = doctextstyle.features.headline.headlines(master72_text_flat)
    assert len(headlines) == 3
    assert headlines[0][0] == 15.96, str(headlines)
    assert headlines[1][0] == 14.04, str(headlines)
    assert headlines[2][0] == 12.0, str(headlines)

    headlines = doctextstyle.features.headline.headlines(
        master72_text_flat,
        headline_start=False,
        returncluster=True,
    )
    assert len(headlines) == 2, str(headlines)
