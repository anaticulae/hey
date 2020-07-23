# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import doctextstyle.data
import doctextstyle.extractor
import doctextstyle.serialize


def test_doctextstyle_dump_load():
    result = doctextstyle.data.DocTextStyle()
    assert result

    dumped = doctextstyle.serialize.dump_docstyle(result)
    loaded = doctextstyle.serialize.load_docstyle(dumped)
    assert loaded == result


def test_doctextstyle_extract():
    source = power.link(power.MASTER098_PDF)
    result = doctextstyle.extractor.extract(source)
    assert result

    assert result.text_size == 12.0
    assert result.pagenumber_size == 12.0
    assert result.footnote_size == 9.0
    assert result.footnote_distance == 10.3

    # justified text
    assert result.text_alignment == 1
