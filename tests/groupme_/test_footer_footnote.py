# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import groupme.footer.footnotes
import tests.fixtures.footnotes


@pytest.mark.parametrize('example', [
    tests.fixtures.footnotes.FOOTNOTES,
    tests.fixtures.footnotes.FOOTNOTES_SECOND,
])
def test_groupme_footer_footenote_parse_notes(example):
    raw, expected_footnotes = example[0], example[1]
    raw = utila.NEWLINE.join(raw)

    parsed = groupme.footer.footnotes.parse(raw)
    for item in parsed:
        print(item)
    assert len(parsed) == expected_footnotes
