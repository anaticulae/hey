# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import pytest
import serializeraw

import sections.feature.title
import tests.resources
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_fontstore_fixture
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_fixture


def test_load_font_lookup(restructured_fontstore):  #pylint:disable=W0621
    first_font = restructured_fontstore.font(
        number=0,
        container=0,
        line=2,
        char=0,
    )

    assert first_font
    assert isinstance(first_font, iamraw.Font)


# qualitygate for further alogrithm improvements
MIN_TITLE_LIKELIHOOD = 0.70


@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.RESTRUCT, id='restruct'),
    pytest.param(tests.resources.HOWTO_PYPORTING, id='pyporting'),
])
def test_extract_title_likelihood(source):
    document = iamraw.path.text(source)
    fontheader = iamraw.path.fontheader(source)
    fontcontent = iamraw.path.fontcontent(source)

    document = serializeraw.load_document(document)
    fontstore = serializeraw.create_fontstore(fontheader, fontcontent)

    result = sections.feature.title.extract_title_likelihood(
        document,
        fontstore,
    )
    assert result[0].content.value >= MIN_TITLE_LIKELIHOOD
    # as a result of rounding the sum of the likelihoods is not one, but thats
    # not a big problem, hitting the region one is enough.
    result = [item.content.value for item in result]
    assert sum(result) == pytest.approx(1.0, abs=0.05)


def test_dump_and_load_likelhood(
        restructured_text,  #pylint:disable=W0621
        restructured_fontstore,  #pylint:disable=W0621
):
    result = sections.feature.title.extract_title_likelihood(
        restructured_text,
        restructured_fontstore,
    )
    dumped = serializeraw.dump_likelihood(result)
    loaded = serializeraw.load_likelihood(dumped)

    assert loaded == result
