# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw

import hey.textnavigator.style as ts

EXAMPLE = ts.TextInfo(
    text=('aller Internetnutzer1 waren im Jahr 2013'
          ' auf entsprechenden Seiten angemeldet und'),
    bounding=iamraw.BoundingBox(x0=113.42, y0=163.65, x1=527.52, y1=177.33),
    style=ts.TextStyle(
        content=[
            ts.CharStyle(start=0, end=20, size=12.0, rise=0.0),
            ts.CharStyle(start=20, end=21, size=8.04, rise=6.37),
            ts.CharStyle(start=21, end=82, size=12.0, rise=0.0),
            # high standing `d` of `und`
            ts.CharStyle(start=82, end=83, size=12.0, rise=6.0),
        ],),
)


def test_textnavigator_style_highnotes():
    parsed = ts.highnotes(EXAMPLE)
    expected = [ts.HighNote(start=20, end=21, value=1)]
    assert parsed == expected, parsed


def test_textnavigator_style_dump_and_load_highnotes():
    highnotes = [
        ts.PageContentTextItems(
            page=2,
            content=[
                ts.HighNote(start=20, end=21, value=1),
                ts.HighNote(start=80, end=81, value=3),
                ts.HighNote(start=120, end=121, value=5),
            ],
        ),
        ts.PageContentTextItems(
            page=5,
            content=[
                ts.HighNote(start=80, end=81, value=3),
                ts.HighNote(start=120, end=121, value=5),
            ],
        )
    ]
    dumped = ts.dump_highnotes(highnotes)
    loaded = ts.load_highnotes(dumped)

    assert loaded == highnotes
