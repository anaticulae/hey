#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from functools import partial
from os.path import exists
from os.path import join

from iamraw import Document
from iamraw import Page
from iamraw import TextContainer
from pytest import fixture
from pytest import mark
from serializeraw import dump_toc
from serializeraw import load_document
from utila import file_read
from utila import run_command

from groupme import ROOT
from groupme.command import PROCESS_NAME
from groupme.command import main
from groupme.feature.chapter import chapter_to_yaml
from groupme.feature.chapter import toc

TEST_DATA = join(ROOT, 'tests/groupme_/data')

assert exists(TEST_DATA), TEST_DATA

SIMPLE = join(TEST_DATA, 'simple')

SIMPLE_PAGESIZE = join(SIMPLE, 'rawmaker__border_pages.yaml')
SIMPLE_POSITION = join(SIMPLE, 'rawmaker__text_positions.yaml')
SIMPLE_TEXT = join(SIMPLE, 'rawmaker__text_text.yaml')
SIMPLE_TOC = join(SIMPLE, 'rawmaker__toc.yaml')
SIMPLE_HORIZONTAL = join(SIMPLE, 'rawmaker__boxes_horizontal.yaml')

for item in [
        SIMPLE,
        SIMPLE_HORIZONTAL,
        SIMPLE_PAGESIZE,
        SIMPLE_POSITION,
        SIMPLE_TEXT,
        SIMPLE_TOC,
]:
    msg = 'missing resource: %s' % item
    assert exists(item), item

HEADLINES_PAGE_3 = 4
TOC_LINES = 12


@fixture
def document() -> Document:
    doc: Document = load_document(SIMPLE_TEXT)
    return doc


@fixture
def page_0(document: Document) -> Page:  # pylint: disable=W0621
    page: Page = document.pages[0]
    return page


@fixture
def page_2(document: Document) -> Page:  # pylint: disable=W0621
    page: Page = document.pages[2]
    return page


@fixture
def page_2_text_only(page_2: Page):  # pylint: disable=W0621
    lines = []
    for child in page_2.children:
        if not isinstance(child, TextContainer):
            continue
        lines.extend(child.text.splitlines())
    return lines


#pylint: disable=invalid-name
run_success = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

run_failure = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)
