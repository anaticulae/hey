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

    sentences = list(words.text.sentence.visit_sentences(firstpage))
    assert len(sentences) == 17


def test_words_text_seventytwo_visit_chapters():
    required = fseventytwo.textrequired(pages=tuple(range(0, 14)))
    pages = words.text.chapter.split(required)

    chapters = list(words.text.sentence.visit_chapters(pages))
    # for headline, content in chapters:
    #     print(headline)
    #     for item in content:
    #         print(item)
    #     print()

    # '1.  Einleitung'
    # '1.1  Fragestellung und Zielsetzung'
    # '1.2  Aufbau der Arbeit'
    # '2.  Das Social Web und die Privatsphre '
    # '2.1  Web  2.0,  Social  Web  und  Social  Media:  Abgrenzungen  und'
    # '2.2  Merkmale von Social Network Sites'
    # '2.3  Eigenschaften netzbasierter Kommunikation'
    # '2.4  Einfhrung in das Konzept der Privatheit'
    assert len(chapters) == 8


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
