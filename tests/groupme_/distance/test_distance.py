# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power

import groupme.feature.distance
import groupme.path


def pyporting(pages: tuple = None):
    source = power.link(power.DOCU07_PDF)
    area = groupme.path.area(source)
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    loaded = groupme.feature.distance.load(
        area,
        text,
        textposition,
        pages=pages,
    )
    return loaded


def test_distance_pyport_page0():
    loaded = pyporting(pages=(0))
    distances = groupme.feature.distance.determine_distances(loaded)
    first = distances[0].content[0]
    assert first.after >= 40, first.after
    assert first.before <= -16, first.before


def test_distance_pyport_page3():
    loaded = pyporting(pages=(3))
    distances = groupme.feature.distance.determine_distances(loaded)
    page = distances[0].content
    assert len(page) == 1, page
    first = page[0]
    assert first.before < 0, first
    assert first.after > 0, first


def test_distance_pyport_page5():
    loaded = pyporting(pages=(5))
    distances = groupme.feature.distance.determine_distances(loaded)
    page = distances[0].content
    assert len(page) == 4, page
    assert all((item.after is None or item.after >= 0.0 for item in page))
    assert all((item.before is None or item.before < 0.0 for item in page))


def test_distance_pyport():
    loaded = pyporting()
    distances = groupme.feature.distance.determine_distances(loaded)
    assert len(distances) == 3, distances


def test_distance_dump_load():
    data = pyporting()
    distances = groupme.feature.distance.determine_distances(data)

    dumped = groupme.feature.distance.dump_distance(distances)
    loaded = groupme.feature.distance.load_distance(dumped)
    assert loaded == distances
