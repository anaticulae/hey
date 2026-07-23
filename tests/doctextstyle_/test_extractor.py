# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilo
import utilotest

import doctextstyle
import doctextstyle.features.blockquote


@utilotest.longrun
@utilotest.requires(hoverpower.MASTER098_PDF)
def test_extract_blockquote_dimension():
    path = hoverpower.link(hoverpower.MASTER098_PDF)
    pages = utilo.rtuple(2, 88)
    ptcns = serializeraw.ptcn_frompath(
        path,
        pages=pages,
    )
    parsed = doctextstyle.parser.parses(ptcns)
    flat = doctextstyle.utils.flatten(parsed)

    extracted = doctextstyle.features.blockquote.blockquote_style(flat)
    # blockquote text size
    assert extracted[1] == 9.96  # VALIDATED


@utilotest.nightly
@utilotest.requires(hoverpower.DISS266_PDF)
def test_extract_headlines_fromdata():
    source = hoverpower.link(hoverpower.DISS266_PDF)
    pages = utilo.rtuple(7, 215)
    navigators = serializeraw.ptcn_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    fontstore = serializeraw.fs_frompath(source)
    headlines = doctextstyle.headlines_fromdata(
        navigators,
        fontstore,
        x0_max_diff=0.0,
    )
    assert len(headlines) == 4
