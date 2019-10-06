# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pytest
from iamraw import BoundingBox
from pytest import mark
from pytest import param
from serializeraw import dump_text
from serializeraw import load_headlines
from serializeraw import load_text
from utila import NEWLINE

import tests.resources
from hey.undefined import extract_undefined
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_contentborder
from tests.fixtures.restruct import restructured_headerfooter
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_pagenumbers
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_positions
from tests.fixtures.restruct import restructured_textexample
from tests.resources import RESTRUCT_BOXES
from tests.resources import RESTRUCT_FONT_CONTENT
from tests.resources import RESTRUCT_FONT_HEADER
from tests.resources import RESTRUCT_HORIZONTAL
from tests.resources import RESTRUCT_PAGENUMBERS
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
from words.feature.text import analyze_page
from words.feature.text import fill_headlines
from words.feature.text import prepare_input
from words.feature.text import work


def test_words_text_work(
        restructured_headlines,  # pylint:disable=W0621
):
    headlines = restructured_headlines
    result = work(
        boxes=RESTRUCT_BOXES,
        font_content=RESTRUCT_FONT_CONTENT,
        font_header=RESTRUCT_FONT_HEADER,
        headlines=headlines,
        headerfooters=tests.resources.RESTRUCT_FOOTERS,
        pagesizes=RESTRUCT_PAGESIZE,
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
    )
    assert len(result) > 6000, str(result)


def test_words_text_dump_and_load_text(
        restructured_headlines,  # pylint:disable=W0621
        restructured_textexample,  # pylint:disable=W0621
):
    headlines = restructured_headlines
    textexample = restructured_textexample
    assert textexample is not None
    assert headlines is not None
    headlines = load_headlines(headlines)

    dumped = dump_text(restructured_textexample)
    loaded = load_text(dumped, headlines)

    for first, second in zip(loaded, textexample):
        assert first == second, '\n\n%s\n%s\n\n\n' % (first, second)
    assert loaded == textexample


@pytest.mark.xfail(reason='require to implement 2 strategies')
def test_words_text_extractor_titles(
        restructured_textexample,  # pylint:disable=W0621
):
    result = restructured_textexample

    # page6
    assert result[0][1][0][0].text == 'CHAPTER 1'
    assert result[0][1][1][0].text == 'RestructuredText Tutorial'

    # page8
    assert result[1][1][0][0].text == 'CHAPTER 2'
    assert result[1][1][1][0].text == 'RestructuredText Guide'
    assert result[1][1][2][0].text == 'Basics'

    # page9
    assert result[2][1][0][0].text == 'Blockquotes'
    assert result[2][1][1][0].text == 'Code: Block'

    # page10
    assert result[3][1][0][0].text == 'CHAPTER 3'
    assert result[3][1][1][0].text == 'RestructuredText Customizations'

    # page12
    assert result[4][1][0][0].text == 'CHAPTER 4'
    assert result[4][1][1][0].text == 'Sphinx Tutorial'
    assert result[4][1][2][0].text == 'Step 1'

    # page13
    assert result[5][1][0][0].text is None

    # page14
    assert result[6][1][0][0].text == 'Documenting a Project'

    #page15
    assert result[7][1][0][0].text is None
    assert result[7][1][1][0].text == 'Aside: Other formats'

    #page16
    assert result[8][1][0][0].text is None
    assert result[8][1][1][0].text == 'Step 2'
    assert result[8][1][2][0].text == 'Referencing Code'

    #page17
    assert result[9][1][0][0].text is None

    #page18
    assert result[10][1][0][0].text == 'CHAPTER 5'
    assert result[10][1][1][0].text == 'Sphinx Guide'


@mark.parametrize(
    'current_page,current_headline,expected_start,expected_end',
    [
        param(
            8,
            2,
            ([]),  # no content after headline
            ('u18'),
            id='page 8',
        ),
        param(
            13,
            7,
            ('Getting Started'),
            ('make html is the main way you will '
             'build HTML documentation locally. It is simply a wrapper '
             'around a more complex call to Sphinx.'),
            id='page 13',
        ),
        param(
            14,
            8,
            ('Now that we have our basic skeleton, let’s document the project. '
             'As you might have guessed from the name, we’ll be documenting a'
             ' basic web crawler.'),
            ('Include the following in your install.rst:'),
            id='page 14',
            marks=pytest.mark.xfail(reason='require selective approach'),
        ),
        param(
            15,
            9,
            ('u0'),
            (None),
            id='page 15',
            marks=pytest.mark.xfail(reason='require selective approach'),
        ),
        param(
            16,
            10,
            ('Make a manpage'),
            ('u21'),
            id='page 16',
        ),
    ])
def test_words_extract_texts_page_x(
        current_page,
        current_headline,
        expected_start,
        expected_end,
        restructured_headlines,  # pylint:disable=W0621
):
    headlines = restructured_headlines
    border, fontstore, headlines, textnavigators, boxes = prepare_input(
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        headlines=headlines,
        pagesizes=RESTRUCT_PAGESIZE,
        headerfooters=tests.resources.RESTRUCT_FOOTERS,
        boxes=RESTRUCT_BOXES,
    )

    def join_output(paragraph):
        try:
            joined = ''.join([item for (item, _) in paragraph.content])
            return joined.replace(NEWLINE, ' ')
        except TypeError:
            return 'u%d' % paragraph.container

    # fill headlines
    headlines = fill_headlines(headlines)
    # ensure that all collect headlines are from page `current_page`
    current = headlines[current_headline]
    assert all([item.page == current_page for item in current])

    analyzed = analyze_page(current, fontstore, textnavigators, border, boxes)
    page, (content) = analyzed
    assert page == current_page, 'wrong extracted page: %d' % page

    first_headline, first_output = content[0][0], content[0][1]
    last_headline, last_output = content[-1][0], content[-1][1]
    # msg = 'invalid returned value due `analyze_page`'
    # assert headline.text == current[0].text, '%s\n%s' % (msg, output)
    assert first_headline.page == current_page
    assert last_headline.page == current_page

    if expected_start == []:
        # empty content on Headlines without content is possible
        assert first_output == expected_start
    else:
        assert first_output, str(first_output)
        first_line = join_output(first_output[0])
        assert first_line == expected_start

    last_line = join_output(last_output[-1]) if last_output else None
    assert last_line == expected_end


def test_words_text_convert_undefined_to_text(
        restructured_headlines,  # pylint:disable=W0621
        restructured_textexample,  # pylint:disable=W0621
        restructured_text,  # pylint:disable=W0621
        restructured_text_positions,  # pylint:disable=W0621
        restructured_sizeandborder,  # pylint:disable=W0621
        restructured_contentborder,
):
    headlines = restructured_headlines
    textexample = restructured_textexample
    text = restructured_text
    text_positions = restructured_text_positions
    contentborder = restructured_contentborder
    assert textexample is not None
    assert headlines is not None
    headlines = load_headlines(headlines)

    dumped = dump_text(restructured_textexample)
    loaded = load_text(dumped, headlines)

    undefined = extract_undefined(
        loaded,
        text,
        text_positions,
        contentborder=contentborder,
    )
    expected = [
        (24, 1, (
            [(0, [
                (BoundingBox(x0=88.44, y0=332.13, x1=133.28, y1=344.13),
                 '• genindex'),
                (BoundingBox(x0=88.44, y0=350.07, x1=136.61, y1=362.07),
                 '• modindex'),
                (BoundingBox(x0=88.44, y0=368.00, x1=122.35, y1=380.00),
                 '• search'),
            ])],
            [[2, 3, 4]],
        )),
    ]
    last_item = undefined[-1]

    assert last_item == expected
