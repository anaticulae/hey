# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw

import groupme.feature.toc
import tests.resources
# pylint: disable=unused-import
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_page_0
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TOC_LINES
from tests.resources import SIMPLE_TEXT
from tests.resources import SIMPLE_TOC_LINES


def test_groupme_toc_groupby_level():
    """Ensure that every section have an textbody"""
    doc = serializeraw.load_document(SIMPLE_TEXT)
    tableofcontent = groupme.feature.toc.toc(doc)
    result = groupme.feature.toc.groupby_level(tableofcontent)
    assert result
    dumped = serializeraw.dump_toc(result)
    assert dumped


def test_extract_toc(simple_page_0: iamraw.Page):  # pylint: disable=W0621
    result = groupme.feature.toc.toc_from_page(simple_page_0)
    assert len(result) == SIMPLE_TOC_LINES


def test_extract_toc_from_document(simple_document: iamraw.Document):  # pylint: disable=W0621
    tableofcontent = groupme.feature.toc.toc(simple_document)

    assert len(tableofcontent) == SIMPLE_TOC_LINES


def test_extract_toc_from_restructured():
    document = serializeraw.load_document(
        tests.resources.RESTRUCT_ONELINE_TEXT,
        pages=(2),
    )
    tocs = groupme.feature.toc.toc(document)
    assert len(tocs) == RESTRUCT_TOC_LINES, str(tocs)
