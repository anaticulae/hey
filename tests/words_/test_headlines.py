# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import iamraw
import pytest
import serializeraw
import utila

import hey.textnavigator.navigator
import tests.fixtures.headlines
import tests.resources
import words.feature.headlines
import words.headlines
import words.headlines.nolevel
# pylint:disable=ungrouped-imports
# pylint:disable=unused-import
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_headerfooter
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_sections
from tests.fixtures.restruct import restructured_sections_manual
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_positions

# NOTE: WHAT SHOULD WE DO WITH THE RAW_LEVEL?
EXPECTED = [
    [
        iamraw.Headline(
            text='CHAPTER 1',
            level=1,
            rawlevel=None,
            container=0,
            page=6,
        ),
        iamraw.Headline(
            text='RestructuredText Tutorial',
            level=2,
            rawlevel=None,
            container=1,
            page=6,
        ),
    ],
    [
        iamraw.Headline(
            text='CHAPTER 2',
            level=1,
            rawlevel=None,
            container=0,
            page=8,
        ),
        iamraw.Headline(
            text='RestructuredText Guide',
            level=2,
            rawlevel=None,
            container=1,
            page=8,
        ),
        iamraw.Headline(
            text='Basics',
            level=3,
            rawlevel=None,
            container=2,
            page=8,
        ),
        iamraw.Headline(
            text='Blockquotes',
            level=3,
            rawlevel=None,
            container=1,
            page=9,
        ),
        iamraw.Headline(
            text='Code: Block',
            level=3,
            rawlevel=None,
            container=10,
            page=9,
        ),
    ],
]


def test_words_headlines_extract_headlines(
        # pylint:disable=W0621
        restructured_sections_manual,
        restructured_text_positions,
        restructured_text,
        restructured_fontstore,
        restructured_sizeandborder,
        restructured_headerfooter,
):
    # TODO: Require new approach, may look into table of content
    sections = restructured_sections_manual
    position = restructured_text_positions
    document = restructured_text
    sizeandborder = restructured_sizeandborder
    headerfooters = restructured_headerfooter

    navigator = hey.textnavigator.navigator.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    extractor = words.headlines.nolevel.NoLevelHeadlineExtractor(
        sectionlist=sections,
        pagetextnavigators=navigator,
        fontstore=restructured_fontstore,
        sizeandborder=sizeandborder,
        headerfooters=headerfooters,
        chapters=[0, 1],
    )
    extracted = extractor.result()
    assert len(extracted) == len(EXPECTED)

    assert [len(item) for item in extracted] == [len(item) for item in EXPECTED]
    assert extracted == EXPECTED


def test_words_headlines_work():
    sections_ = restructured_sections()
    dumped = words.feature.headlines.work(
        boxes=tests.resources.boxed(tests.resources.RESTRUCT),
        font_content=tests.resources.font_content(tests.resources.RESTRUCT),
        font_header=tests.resources.font_header(tests.resources.RESTRUCT),
        headerfooters=tests.resources.headerfooters(tests.resources.RESTRUCT),
        sections=sections_,
        sizeandborder=tests.resources.sizeandborder(tests.resources.RESTRUCT),
        text=tests.resources.text(tests.resources.RESTRUCT),
        text_position=tests.resources.text_positions(tests.resources.RESTRUCT),
    )
    # dump some headlines
    assert len(dumped) > 2100, str(dumped)


def test_words_headlines_dump_and_load_headlines():
    """Dump and load the example above"""
    dumped = serializeraw.dump_headlines(EXPECTED)
    loaded = serializeraw.load_headlines(dumped)

    assert loaded == EXPECTED


def extract_master72_headlines(root: str):
    master72 = tests.resources.MASTER_72PAGES
    sections = tests.resources.sections(master72)
    text = tests.resources.text(master72)
    text_positions = tests.resources.text_positions(master72)
    font_header = tests.resources.font_header(master72)
    font_content = tests.resources.font_content(master72)
    sizeandborder = tests.resources.sizeandborder(master72)
    boxed = tests.resources.boxed(master72)
    headerfooters = tests.resources.headerfooters(master72)

    headlines = words.feature.headlines.work(
        sections,
        text,
        text_positions,
        font_header,
        font_content,
        sizeandborder,
        boxes=boxed,
        headerfooters=headerfooters,
    )
    headlines_outpath = os.path.join(root, 'headlines_result.yaml')
    utila.file_create(headlines_outpath, headlines)

    assert len(headlines) > 400, str(headlines)
    result = serializeraw.load_headlines(headlines)

    return result


def test_words_features_headlines_work_master72pages(testdir):
    root = str(testdir)
    headlines_loaded = extract_master72_headlines(root)

    # TODO: CHANGE AFTER SUPPORTING LITERATURVERZEICH AND ERKLARUNG
    assert len(headlines_loaded) == 5, str(headlines_loaded)

    expected_headlines = [
        '1.  Einleitung',
        '2.  Das Social Web und die Privatsphäre –',
        '3.  Systemtheorie und moderne Netzwerksoziologie –',
        '4.  Privatheit  und  Identitätsbildung  im  Social  Web  –',
        '5.  Schlussbetrachtung und Fazit',
    ]
    # headlines of first element in section
    headlines_text = [item[0].text for item in headlines_loaded]
    assert headlines_text == expected_headlines, str(headlines_text)


@pytest.mark.xfail(reason='headline extractor is broken')
def test_words_features_headlines_work_master72pages_subsections(testdir):
    root = str(testdir)
    headlines_loaded = extract_master72_headlines(root)
    expected_subsection_count = [2, 8, 10, 5, 2]

    subsections = [item[1:] for item in headlines_loaded]
    subsections_count = [len(item) for item in subsections]

    assert subsections_count == expected_subsection_count


def test_words_features_headlines_filter_headlines():
    example = tests.fixtures.headlines.EXAMPLE

    filtered = words.headlines.standard.filter_headlines(example)

    filtered = [item for item in filtered.values()]  # dict to list

    subsections = [item[1:] for item in filtered]
    subsections_count = [len(item) for item in subsections]
    expected_subsection_count = [2, 5, 7, 5, 2]

    assert subsections_count == expected_subsection_count
