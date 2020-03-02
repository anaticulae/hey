# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw
import pytest
import serializeraw
import texmex

EXAMPLE = texmex.TextInfo(
    text=('aller Internetnutzer1 waren im Jahr 2013'
          ' auf entsprechenden Seiten angemeldet und'),
    bounding=iamraw.BoundingBox(x0=113.42, y0=163.65, x1=527.52, y1=177.33),
    style=texmex.TextStyle(
        content=[
            texmex.CharStyle(start=0, end=20, size=12.0, rise=0.0),
            texmex.CharStyle(start=20, end=21, size=8.04, rise=6.37),
            texmex.CharStyle(start=21, end=82, size=12.0, rise=0.0),
            # high standing `d` of `und`
            texmex.CharStyle(start=82, end=83, size=12.0, rise=6.0),
        ],),
)


def test_textnavigator_style_highnotes():
    parsed = texmex.highnotes(EXAMPLE)
    expected = [texmex.HighNote(start=20, end=21, value=1)]
    assert parsed == expected, parsed


def test_textnavigator_style_highnotes_remove_highnotes():
    removed = texmex.remove_highnotes(EXAMPLE)
    expected = EXAMPLE.text[0:20] + EXAMPLE.text[21:]
    assert removed == expected


@pytest.mark.parametrize('expected, merge', [
    (
        texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=20, size=12.0, rise=0.0),
            texmex.CharStyle(start=20, end=81, size=12.0, rise=0.0),
            texmex.CharStyle(start=81, end=82, size=12.0, rise=6.0),
        ]),
        False,
    ),
    (
        texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=81, size=12.0, rise=0.0),
            texmex.CharStyle(start=81, end=82, size=12.0, rise=6.0),
        ]),
        True,
    ),
])
def test_textnavigator_style_remove_hightnotes(expected, merge):
    clean = texmex.style_without_highnotes(EXAMPLE, merge=merge)
    assert clean == expected


def test_textnavigator_style_dump_and_load_highnotes():
    highnotes = [
        texmex.PageContentTextItems(
            page=2,
            content=[
                texmex.HighNote(start=20, end=21, value=1),
                texmex.HighNote(start=80, end=81, value=3),
                texmex.HighNote(start=120, end=121, value=5),
            ],
        ),
        texmex.PageContentTextItems(
            page=5,
            content=[
                texmex.HighNote(start=80, end=81, value=3),
                texmex.HighNote(start=120, end=121, value=5),
            ],
        )
    ]
    dumped = serializeraw.dump_highnotes(highnotes)
    loaded = serializeraw.load_highnotes(dumped)

    assert loaded == highnotes
