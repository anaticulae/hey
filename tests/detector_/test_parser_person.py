# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark

from detector.parser.person import Person
from detector.parser.person import Title
from detector.parser.person import order_persons
from detector.parser.person import parse

PROF_DR = Title.PROF | Title.DR

HELMUT = Person(
    Title.BSC,
    'Fahrendholz',
    'Helmut Konrad',
    'B.Sc. Helmut Konrad Fahrendholz',
)

GOMEZ = Person(
    PROF_DR,
    'Gomez',
    'Fabian',
    'Hochschullehrer: Prof. Dr.-Ing. Fabian Gomez',
)

KAHN = Person(
    PROF_DR,
    'Kahn',
    'Oliver',
    'Zweitgutachter: Prof. Dr. Oliver Kahn',
)


@mark.parametrize('raw, expected', [
    (
        'B.Sc. Helmut Konrad Fahrendholz',
        Person(
            Title.BSC,
            'Fahrendholz',
            'Helmut Konrad',
            'B.Sc. Helmut Konrad Fahrendholz',
        ),
    ),
    (
        'Hochschullehrer: Prof. Dr.-Ing. Fabian Gomez',
        Person(
            PROF_DR,
            'Gomez',
            'Fabian',
            'Prof. Dr.-Ing. Fabian Gomez',
        ),
    ),
    (
        'Zweitgutachter: Prof. Dr. Oliver Kahn  ',
        Person(
            PROF_DR,
            'Kahn',
            'Oliver',
            'Prof. Dr. Oliver Kahn',
        ),
    ),
    (
        'Betreuer VAI:Dipl. Ing. Andreas Zickler   Hier folgt weiterer Text',
        Person(
            Title.MASTER,
            'Zickler',
            'Andreas',
            'Betreuer VAI:Dipl. Ing. Andreas Zickler',
        ),
    ),
    (
        'Betreuer: Prof. Dr. Groeg Trichter  ',
        Person(
            PROF_DR,
            'Trichter',
            'Groeg',
            'Betreuer: Prof. Dr. Groeg Trichter',
        ),
    ),
])
def test_parse_person(raw, expected):
    parsed = parse(raw)
    assert parsed == expected, str(parsed)


def test_parser_person_order_person():
    persons = [KAHN, GOMEZ, HELMUT]
    expected = (HELMUT, [GOMEZ, KAHN])

    current = order_persons(persons)

    assert current == expected, str(current)
