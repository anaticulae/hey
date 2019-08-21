# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from detector.parser.title import parse
from tests.detector_.titlepage.example import new_fontstore
from tests.detector_.titlepage.example import new_textnavgiator


def test_detector_parse_title():
    textnavigator = new_textnavgiator()
    # print(textnavigator)
    parse(textnavigator)

    # parse
