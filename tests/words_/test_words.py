# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
from pytest import fixture
from serializeraw import dump_text
from serializeraw import load_headlines
from serializeraw import load_text

# pylint:disable=W0611
from tests.fixtures.restruct import restructured_boxed
from tests.fixtures.restruct import restructured_boxed_dumped
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_list_dumped
from tests.fixtures.restruct import restructured_list_work
from tests.fixtures.restruct import restructured_textexample
from tests.fixtures.restruct import restructured_textexample_dumped
from words.feature.word import load_resources
from words.feature.word import process_words
from words.feature.word import work


@fixture
def restructured_words(
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
    text, listlookup, boxlookup = load_resources(
        boxed=boxed,
        headlines=headlines,
        lists=lists,
        text=text,
    )

    result = process_words(text, listlookup, boxlookup)
    assert result
    return result


def test_words_dump_and_load_words_result(
        restructured_words,
        restructured_headlines,
):
    # TODO: check completness of this test
    headlines = restructured_headlines
    dumped = dump_text(restructured_words)
    headlines = load_headlines(headlines)
    loaded = load_text(dumped, headlines)
    assert loaded == restructured_words
