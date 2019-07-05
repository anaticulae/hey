# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture

from tests.resources import RESTRUCT_BOXES
from tests.resources import RESTRUCT_FONT_CONTENT
from tests.resources import RESTRUCT_FONT_HEADER
from tests.resources import RESTRUCT_HORIZONTAL
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
# pylint:disable=W0611
from tests.words_.test_headlines import restrucutured_headlines
from words.feature.headlines import load_headlines
from words.feature.text import dump_text
from words.feature.text import extract_texts
from words.feature.text import load_text
from words.feature.text import prepare_input
from words.feature.text import work


def test_word_text_work(restrucutured_headlines):
    headlines = restrucutured_headlines
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
def textexample(restrucutured_headlines):
    headlines = restrucutured_headlines
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


def test_word_text_dump_and_load_text(textexample, restrucutured_headlines):
    headlines = restrucutured_headlines
    assert textexample is not None
    assert headlines is not None
    headlines = load_headlines(headlines)

    dumped = dump_text(textexample)
    loaded = load_text(dumped, headlines)

    for first, second in zip(loaded, textexample):
        assert first == second, '\n\n%s\n%s\n\n\n' % (first, second)
    assert loaded == textexample


def test_word_text_extractor_titles(textexample):
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

    # page14
    assert result[5][1][0][0].text == 'Documenting a Project'

    #page15
    assert result[6][1][0][0].text is None
    assert result[6][1][1][0].text == 'Aside: Other formats'
