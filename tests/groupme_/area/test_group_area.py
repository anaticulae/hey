# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import linero.path
import power
import utila

import groupme.feature.area


def pyporting(pages: tuple = None):
    source = power.link(power.DOCU07_PDF)
    text = iamraw.path.text(source)
    textpositions = iamraw.path.textposition(source)
    tables = linero.path.table(source)
    boxes = iamraw.path.boxed(source)
    loaded = groupme.feature.area.load(
        boxes=boxes,
        tables=tables,
        text=text,
        textpositions=textpositions,
        pages=pages,
    )
    return loaded


def test_groupme_area_pyporting_table():
    loaded = pyporting(pages=3)
    grouped = groupme.feature.area.group_areas(loaded)
    assert grouped
    assert len(grouped[0].outside['tables']) == 6


def test_groupme_area_pyporting_boxes():
    loaded = pyporting(pages=5)
    grouped = groupme.feature.area.group_areas(loaded)
    assert grouped
    assert len(grouped) == 1
    # elements inside boxes
    assert len(grouped[0].outside['boxes']) == 17


def test_groupme_area_dump_load():
    data = pyporting()
    grouped = groupme.feature.area.group_areas(data)

    assert grouped
    dumped = groupme.feature.area.dump_area(grouped)
    loaded = groupme.feature.area.load_area(dumped)
    assert grouped == loaded


def test_groupme_area_rectangle_merge():
    before = [
        (10, 10, 100, 100),
        (10, 10, 30, 30),
        (90, 10, 150, 100),
        (30, 30, 60, 70),
    ]
    expected = [
        (10, 10, 100, 100),
        (90, 10, 150, 100),
    ]

    merged = utila.rectangle_merge(before)
    assert merged == expected

    before = [
        (10, 10, 100, 100),
        (25, 25, 50, 50),
        (50, 50, 75, 75),
        (75, 75, 100, 100),
    ]
    expected = [
        (10, 10, 100, 100),
    ]

    merged = utila.rectangle_merge(before)
    assert merged == expected
