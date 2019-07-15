# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# pylint:disable=W0611
from tests.fixtures.restruct import restructured_boxed
from tests.fixtures.restruct import restructured_boxed_dumped
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_list_dumped
from tests.fixtures.restruct import restructured_list_work
from tests.fixtures.restruct import restructured_textexample
from tests.fixtures.restruct import restructured_textexample_dumped
from words.feature.words import work


def test_words_work(
        # pylint:disable=W0621
        restructured_boxed_dumped,
        restructured_list_dumped,
        restructured_headlines,
        restructured_textexample_dumped,
):
    text = restructured_textexample_dumped
    headlines = restructured_headlines
    boxed = restructured_boxed_dumped
    lists = restructured_list_dumped
    # dumped data as input
    for item in [
            boxed,
            headlines,
            lists,
            text,
    ]:
        assert isinstance(item, str), str(item)

    # compare text, headlines, lists and boxes to one output
    dumped = work(
        boxed=boxed,
        headlines=headlines,
        lists=lists,
        text=text,
    )
    assert len(dumped) > 2000, str(dumped)
