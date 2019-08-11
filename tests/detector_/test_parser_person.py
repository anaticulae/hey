# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark
from pytest import param

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
        '  B.Sc. Helmut Konrad Fahrendholz',
        HELMUT,
    ),
    (
        'Hochschullehrer: Prof. Dr.-Ing. Fabian Gomez',
        GOMEZ,
    ),
    (
        '  Zweitgutachter: Prof. Dr. Oliver Kahn  ',
        KAHN,
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
    (
        '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        Person(
            Title.DR,
            'Contemporary',
            'Dirk',
            '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        ),
    ),
    param(
        '   vorgelegt von Thomas Helmer    ',
        Person(
            Title.NO_TITLE,
            'Helmer',
            'Thomas',
            'vorgelegt von Thomas Helmer',
        ),
        marks=mark.xfail(reason='unsupported in current regex impl'),
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
