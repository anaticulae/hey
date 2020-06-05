# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import detector.bibliography.data as dbd


def test_sort_byname():
    example = [
        dbd.BibliographyReference.create('Mueller Erwin'),
        dbd.BibliographyReference.create('Arnold Anton'),
        dbd.BibliographyReference.create('Fahrendholz Konrad'),
    ]
    result = dbd.theissen_sort(example)
    expected = [example[1], example[2], example[0]]
    assert result == expected


def test_sort_byyear():
    year = [
        dbd.BibliographyReference.create('Fahrendholz Konrad', year=2016),
        dbd.BibliographyReference.create('Fahrendholz Konrad', year=None),
        dbd.BibliographyReference.create('Fahrendholz Konrad', year=1987),
    ]
    result = dbd.theissen_sort(year)
    expected = [year[2], year[0], year[1]]
    assert result == expected


def test_sort_bynoname():
    # pylint:disable=C0103
    ov = [
        dbd.BibliographyReference(year=None),
        dbd.BibliographyReference(year=2016),
        dbd.BibliographyReference.create('Fahrendholz Konrad', year=None),
        dbd.BibliographyReference.create('Fahrendholz Konrad', year=1987),
    ]
    result = dbd.theissen_sort(ov)
    expected = [ov[3], ov[2], ov[1], ov[0]]
    assert result == expected
