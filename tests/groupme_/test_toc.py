# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import Document
from iamraw import Page
from serializeraw import load_document

from groupme.feature.toc import toc
from groupme.feature.toc import toc_from_page
from groupme.feature.toc import toc_to_yaml
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TOC_LINES
from tests.resources import SIMPLE_TEXT
from tests.resources import SIMPLE_TOC_LINES
from tests.resources import simpledocument  # pylint: disable=unused-import
from tests.resources import simplepage_0  # pylint: disable=unused-import


def test_toc_to_yaml():
    """Ensure that every section have an textbody"""
    doc = load_document(SIMPLE_TEXT)
    tableofcontent = toc(doc)
    result = toc_to_yaml(tableofcontent)
    assert result


def test_extract_toc(simplepage_0: Page):  # pylint: disable=W0621
    result = toc_from_page(simplepage_0)
    assert len(result) == SIMPLE_TOC_LINES


def test_extract_toc_from_document(simpledocument: Document):  # pylint: disable=W0621
    tableofcontent = toc(simpledocument)
    assert len(tableofcontent) == SIMPLE_TOC_LINES


def test_extract_toc_from_restructured():
    document = load_document(RESTRUCT_TEXT)
    tocs = toc(document)
    assert len(tocs) == RESTRUCT_TOC_LINES
