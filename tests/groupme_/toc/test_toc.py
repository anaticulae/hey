# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw
import utila

import groupme.feature.toc
import groupme.toc.loader
import tests.resources
# pylint: disable=unused-import
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_page_0
from tests.resources import RESTRUCT_TOC_LINES
from tests.resources import SIMPLE
from tests.resources import SIMPLE_TEXT
from tests.resources import SIMPLE_TOC_LINES


def test_groupme_toc_groupby_level():
    navigators = groupme.toc.loader.load_frompath(SIMPLE)
    selected = groupme.feature.toc.select_tocpages(navigators)
    # select toc pages only
    navigators = [item for item in navigators if item.page in selected]
    loaded = groupme.toc.strategy.load(navigators)
    tableofcontent = groupme.toc.extractor.extract(loaded)

    tableofcontent = utila.flatten(tableofcontent.content)
    result = groupme.feature.toc.groupby_level(tableofcontent)
    assert result
    dumped = serializeraw.dump_toc(result)
    assert dumped
    # TODO: Check level content


def test_extract_toc(simple_page_0: iamraw.Page):  # pylint: disable=W0621
    result = groupme.feature.toc.toc_from_page(simple_page_0)
    assert len(result) == SIMPLE_TOC_LINES


@pytest.mark.parametrize('resources, pages, expected', [
    pytest.param(
        tests.resources.RESTRUCT,
        (2),
        RESTRUCT_TOC_LINES,
        id='restructured',
    ),
    pytest.param(
        tests.resources.SIMPLE,
        (0),
        SIMPLE_TOC_LINES,
        marks=pytest.mark.xfail,
        id='simple',
    ),
])
def test_extract_toc_from_path(resources, pages, expected):
    navigators = groupme.toc.loader.load_frompath(
        resources,
        pages=pages,
    )
    loaded = groupme.toc.strategy.load(navigators)
    extracted = groupme.toc.extractor.extract(loaded)
    flat = utila.flatten(extracted)
    assert len(flat) == expected, str(flat)
