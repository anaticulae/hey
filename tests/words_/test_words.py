# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from serializeraw import load_headlines

# pylint:disable=W0611
from tests.fixtures.restruct import restructured_boxed
from tests.fixtures.restruct import restructured_boxed_dumped
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_list_dumped
from tests.fixtures.restruct import restructured_list_work
from tests.fixtures.restruct import restructured_textexample
from tests.fixtures.restruct import restructured_textexample_dumped
from words.feature.words import dump_text
from words.feature.words import load_text
from words.feature.words import prepare_input
from words.feature.words import process_words
from words.feature.words import work


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
    text, listlookup, boxlookup = prepare_input(
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

    headlines = restructured_headlines
    dumped = dump_text(restructured_words)
    headlines = load_headlines(headlines)
    loaded = load_text(dumped, headlines)
    assert loaded == restructured_words
