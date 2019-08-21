# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from detector.parser.title import TitleParserState
from detector.parser.title import parse
# pylint:disable=W0611
from tests.detector_.titlepage.example import TEXT_TITLE
from tests.detector_.titlepage.example import new_textnavgiator


def test_detector_parse_title(new_textnavgiator):  # pylint:disable=W0621
    textnavigator = new_textnavgiator
    parsed = parse(textnavigator)

    assert parsed == TEXT_TITLE, parsed


def test_detector_parse_title_empty(new_textnavgiator):  # pylint:disable=W0621
    empty_textnavigator = new_textnavgiator
    empty_textnavigator.data.clear()

    parsed = parse(empty_textnavigator)

    assert parsed == TitleParserState.NOT_ENOUGH_LINES
