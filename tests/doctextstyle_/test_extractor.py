# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import doctextstyle.features.blockquote


@utilatest.skip_longrun
def test_extract_blockquote_dimension():
    path = power.link(power.MASTER098_PDF)
    pages = utila.ranged_tuple(2, 88)
    ptcns = serializeraw.create_pagetextcontentnavigators_frompath(
        path,
        pages=pages,
    )
    parsed = doctextstyle.parser.parses(ptcns)
    flat = doctextstyle.utils.flatten(parsed)

    extracted = doctextstyle.features.blockquote.blockquote_style(flat)
    # blockquote text size
    assert extracted[1] == 9.96
