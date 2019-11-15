# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import tests.words_.fixtures.seventytwo as fseventytwo
import words.text.chapter
import words.text.sentence


def test_words_text_seventytwo_extract_texts():
    required = fseventytwo.textrequired(pages=(3))
    extracted = words.text.chapter.extract_texts(required)
    assert extracted

    firstpage = utila.select_page(extracted, 3)
    firstsection = firstpage.content[0]
    sectioncontent = firstsection.content

    assert len(sectioncontent) == 17


def test_words_text_seventytwo_visit_sentences():
    required = fseventytwo.textrequired(pages=(3))
    firstpage = words.text.chapter.split(required)[0]
    required = fseventytwo.textrequired(pages=(4))
    secondpage = words.text.chapter.split(required)[0]

    sentences = list(words.text.sentence.visit_sentences(firstpage))
    assert len(sentences) == 17

    sentences = list(words.text.sentence.visit_sentences(secondpage))
    assert len(sentences) == 14

    # second page first sentence
    assert sentences[0][1] == ('Nutzerverhalten vor allem in '
                               'Bezug auf die Privatheitsthematik.')

    # second page second sentence
    assert sentences[1][1] == ('Massenmedien und Literatur sehen die '
                               'Privatsphäre in Gefahr und äußern daher zum '
                               'Teil massive Kritik an der Selbstpräsentation '
                               'der Nutzer.')


def test_words_text_seventytwo_visit_sentences_merge_page_endstart():
    """Merge the first two content pages to one sentence unit. Important
    is to unite the last sentence of the first page with the first
    sentence of the second page and merge them to one sentence."""
    required = fseventytwo.textrequired(pages=(3, 4))
    pages = words.text.chapter.split(required)

    merged = list(words.text.sentence.merge_sentences(pages))
    assert len(merged) == 30

    merged_middle_sentence = merged[16][1]
    assert merged_middle_sentence == (
        'Kritisch beurteilt wird das '
        'Nutzerverhalten vor allem in Bezug auf die Privatheitsthematik.')


def test_words_text_seventytwo_visit_chapters():
    required = fseventytwo.textrequired(pages=tuple(range(0, 14)))
    pages = words.text.chapter.split(required)

    chapters = list(words.text.sentence.visit_chapters(pages))
    minpage = min([headline.page for headline, _ in chapters])
    assert minpage == 3, minpage
    # '1.  Einleitung'
    # Headline(text=None, level=None, rawlevel=None, page=4, container=-1)
    # '1.1  Fragestellung und Zielsetzung'
    # '1.2  Aufbau der Arbeit'
    # '2.  Das Social Web und die Privatsphre '
    # '2.1  Web  2.0,  Social  Web  und  Social  Media:  Abgrenzungen  und'
    # Headline(text=None, level=None, rawlevel=None, page=7, container=-1)
    # Headline(text=None, level=None, rawlevel=None, page=8, container=-1)
    # Headline(text=None, level=None, rawlevel=None, page=9, container=-1)
    # Headline(text=None, level=None, rawlevel=None, page=10, container=-1)
    # '2.2  Merkmale von Social Network Sites'
    # Headline(text=None, level=None, rawlevel=None, page=11, container=-1)
    # '2.3  Eigenschaften netzbasierter Kommunikation'
    # '2.4  Einfhrung in das Konzept der Privatheit'
    sectionpages = [headline.page for headline, _ in chapters]
    assert sectionpages == [3, 4, 4, 5, 6, 6, 7, 8, 9, 10, 10, 11, 12, 13]
    assert len(chapters) == 14


def test_words_text_seventytwo_extract_sentences():
    expected = fseventytwo.firstpage_sentences()
    raw = ' '.join(expected)
    splitted = words.text.sentence.split_sentences(raw)

    assert len(splitted) == len(expected)
    assert splitted == expected


@pytest.mark.xfail(reason='multiple equal fontdistance, think about later')
def test_words_text_doubleequal_fontdistance():
    required = fseventytwo.textrequired(pages=(0))
    extracted = words.text.chapter.extract_texts(required)
    assert extracted
