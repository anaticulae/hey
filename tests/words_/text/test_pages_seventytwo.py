# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import tests.words_.fixtures.seventytwo as fseventytwo
import words.text.chapter
import words.text.sentence


def test_words_text_seventytwo_extract_texts():
    required = fseventytwo.textrequired(pages=(3))
    extracted = words.text.chapter.extract_texts(required)
    assert extracted


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
