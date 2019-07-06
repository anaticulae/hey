# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from pytest import mark
from pytest import param
from utila import NEWLINE

from tests.resources import RESTRUCT_BOXES
from tests.resources import RESTRUCT_FONT_CONTENT
from tests.resources import RESTRUCT_FONT_HEADER
from tests.resources import RESTRUCT_HORIZONTAL
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
# pylint:disable=W0611
from tests.words_.test_headlines import restructured_headlines
from words.feature.headlines import load_headlines
from words.feature.text import analyze_page
from words.feature.text import dump_text
from words.feature.text import extract_texts
from words.feature.text import fill_headlines
from words.feature.text import load_text
from words.feature.text import prepare_input
from words.feature.text import work


def test_words_text_work(restructured_headlines):
    headlines = restructured_headlines
    result = work(
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_content=RESTRUCT_FONT_CONTENT,
        font_header=RESTRUCT_FONT_HEADER,
        headlines=headlines,
        pagesizes=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
        boxes=RESTRUCT_BOXES,
    )
    assert len(result) > 6000, str(result)


@fixture
def textexample(restructured_headlines):
    headlines = restructured_headlines
    border, fontstore, headlines, textnavigators, boxes = prepare_input(
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        headlines=headlines,
        pagesizes=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
        boxes=RESTRUCT_BOXES,
    )

    extracted = extract_texts(
        border=border,
        fontstore=fontstore,
        headlines=headlines,
        textnavigators=textnavigators,
        boxes=boxes,
    )
    assert extracted is not None
    return extracted


def test_words_text_dump_and_load_text(textexample, restructured_headlines):
    headlines = restructured_headlines
    assert textexample is not None
    assert headlines is not None
    headlines = load_headlines(headlines)

    dumped = dump_text(textexample)
    loaded = load_text(dumped, headlines)

    for first, second in zip(loaded, textexample):
        assert first == second, '\n\n%s\n%s\n\n\n' % (first, second)
    assert loaded == textexample


def test_words_text_extractor_titles(textexample):
    result = textexample
    # [(6, [(Headline(text='CHAPTER 1', level=1, rawlevel=None, page=6,
    #                 container=0), []), (Headline(text='RestructuredText Tutor
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


@mark.parametrize('current_page,current_headline,expected_start,expected_end', [
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
    ),
    param(
        15,
        9,
        ('u0'),
        (None),
        id='page 15',
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
        restructured_headlines,
):
    headlines = restructured_headlines
    border, fontstore, headlines, textnavigators, boxes = prepare_input(
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        headlines=headlines,
        pagesizes=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
        boxes=RESTRUCT_BOXES,
    )

    # fill headlines
    headlines = fill_headlines(headlines)
    # ensure that all collect headlines are from page 13
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

    assert first_output, str(first_output)

    first_line = join_output(first_output[0])
    last_line = join_output(last_output[-1]) if last_output else None
    assert last_line == expected_end
    assert first_line == expected_start


def join_output(paragraph):
    try:
        joined = ''.join([item for (item, _) in paragraph.content])
        return joined.replace(NEWLINE, ' ')
    except TypeError:
        return 'u%d' % paragraph.container
