# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from detector.feature.titlepage import work
from tests.resources import SIMPLE_ONELINE_POSITION
from tests.resources import SIMPLE_ONELINE_TEXT


def test_titlepage_parser():
    extracted = work(SIMPLE_ONELINE_TEXT, SIMPLE_ONELINE_POSITION)
    assert extracted

    # ensure that result is converted to yaml
    assert isinstance(extracted, str), type(extracted)
