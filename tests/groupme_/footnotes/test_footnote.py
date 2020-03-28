# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import groupme.footnotes.parser
import tests.fixtures.footnotes


@pytest.mark.parametrize('example', [
    pytest.param(tests.fixtures.footnotes.FOOTNOTES,),
    pytest.param(tests.fixtures.footnotes.FOOTNOTES_SECOND,),
])
def test_groupme_footer_footenote_parse_notes(example):
    raw, expected_footnotes = example[0], example[1]
    parsed = groupme.footnotes.parser.parse(raw)
    assert len(parsed) == expected_footnotes


def test_groupme_footer_footenote_parse_notes_multiline():
    raw = tests.fixtures.footnotes.FOOTNOTES_SECOND[0]
    parsed = groupme.footnotes.parser.parse(raw)
    assert len(parsed) == 23, len(parsed)

    assert parsed[0].number == 1
    assert parsed[0].text == ('Aus Grnden der besseren Lesbarkeit wird hier '
                              'und im Folgenden ausschlielich die maskuline '
                              'Form verwendet, wobei immer beide '
                              'Geschlechter gemeint sind.')
    assert parsed[-1].number == 23
