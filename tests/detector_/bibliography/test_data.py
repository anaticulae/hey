# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import detector.bibliography.data


def test_sort_byname():
    example = [
        iamraw.BibliographyReference.create('Mueller Erwin'),
        iamraw.BibliographyReference.create('Arnold Anton'),
        iamraw.BibliographyReference.create('Fahrendholz Konrad'),
    ]
    result = detector.bibliography.data.theissen_sort(example)
    expected = [example[1], example[2], example[0]]
    assert result == expected


def test_sort_byyear():
    year = [
        iamraw.BibliographyReference.create('Fahrendholz Konrad', year=2016),
        iamraw.BibliographyReference.create('Fahrendholz Konrad', year=None),
        iamraw.BibliographyReference.create('Fahrendholz Konrad', year=1987),
    ]
    result = detector.bibliography.data.theissen_sort(year)
    expected = [year[2], year[0], year[1]]
    assert result == expected


def test_sort_bynoname():
    # pylint:disable=C0103
    ov = [
        iamraw.BibliographyReference(year=None),
        iamraw.BibliographyReference(year=2016),
        iamraw.BibliographyReference.create('Fahrendholz Konrad', year=None),
        iamraw.BibliographyReference.create('Fahrendholz Konrad', year=1987),
    ]
    result = detector.bibliography.data.theissen_sort(ov)
    expected = [ov[3], ov[2], ov[1], ov[0]]
    assert result == expected
