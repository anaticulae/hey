# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from serializeraw import load_boxes

from tests.fixtures.restruct import RESTRUCT_BOXES
from tests.fixtures.restruct import RESTRUCT_HORIZONTAL
from tests.fixtures.restruct import RESTRUCT_PAGESIZE
from tests.fixtures.restruct import RESTRUCT_TEXT
from tests.fixtures.restruct import RESTRUCT_TEXT_POSITION
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_textexample
from tests.fixtures.restruct import restructured_textexample_dumped
from words.feature.boxed import dump_boxedcontent
from words.feature.boxed import load_boxedcontent
from words.feature.boxed import prepare_input
from words.feature.boxed import process_content
from words.feature.boxed import work


@fixture
def restructured_boxed(
        restructured_textexample_dumped,
        restructured_headlines,
):
    headlines = restructured_headlines
    undefined = restructured_textexample_dumped

    extracted, _ = prepare_input(
        undefined,
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        border=RESTRUCT_PAGESIZE,
        headlines=headlines,
        horizontals=RESTRUCT_HORIZONTAL,
    )
    boxes = load_boxes(RESTRUCT_BOXES)

    result = process_content(extracted, boxes)
    return result


def test_words_boxed_work(restructured_boxed):  # pylint:disable=W0621
    dumped = dump_boxedcontent(restructured_boxed)
    assert len(dumped) > 2000, str(dumped)


def test_words_boxed_dump_and_load(restructured_boxed):  # pylint:disable=W0621
    dumped = dump_boxedcontent(restructured_boxed)

    loaded = load_boxedcontent(dumped)
    assert loaded == restructured_boxed
