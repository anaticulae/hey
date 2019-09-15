# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import detector.parser.person
from detector.parser.person import Title
from detector.parser.person import order_persons
from detector.parser.person import parse

PROF_DR = Title.PROF | Title.DR

HELMUT = iamraw.Person(
    Title.BSC,
    'Fahrendholz',
    'Helmut Konrad',
    'B.Sc. Helmut Konrad Fahrendholz',
)

GOMEZ = iamraw.Person(
    PROF_DR,
    'Gomez',
    'Fabian',
    'Hochschullehrer: Prof. Dr.-Ing. Fabian Gomez',
)

KAHN = iamraw.Person(
    PROF_DR,
    'Kahn',
    'Oliver',
    'Zweitgutachter: Prof. Dr. Oliver Kahn',
)


@pytest.mark.parametrize('raw, expected', [
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
        iamraw.Person(
            Title.MASTER,
            'Zickler',
            'Andreas',
            'Betreuer VAI:Dipl. Ing. Andreas Zickler',
        ),
    ),
    (
        'Betreuer: Prof. Dr. Groeg Trichter  ',
        iamraw.Person(
            PROF_DR,
            'Trichter',
            'Groeg',
            'Betreuer: Prof. Dr. Groeg Trichter',
        ),
    ),
    (
        '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        iamraw.Person(
            Title.DR,
            'Contemporary',
            'Dirk',
            '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        ),
    ),
    (
        'Erstgutachter: Prof. Dr. rer. biol. hum. Erwin Paulat',
        iamraw.Person(
            PROF_DR,
            'Paulat',
            'Erwin',
            'Erstgutachter: Prof. Dr. rer. biol. hum. Erwin Paulat',
        ),
    ),
    (
        'Zweitgutachter: Prof. Dr. med. Dr.-Ing. Ronald Verbus-Trapp',
        iamraw.Person(
            PROF_DR,
            'Verbus-Trapp',
            'Ronald',
            'Zweitgutachter: Prof. Dr. med. Dr.-Ing. Ronald Verbus-Trapp',
        ),
    ),
    (
        '   vorgelegt von   Thomas Helmer  ',
        iamraw.Person(
            Title.NO_TITLE,
            'Helmer',
            'Thomas',
            'vorgelegt von   Thomas Helmer',
        ),
    ),
    (
        'Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt',
        iamraw.Person(
            Title.MASTER,
            'Frühwirt',
            'Stephan',
            'Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt',
        ),
    ),
    (
        'Prof. Dr. Nobert Bolz',
        iamraw.Person(
            PROF_DR,
            'Bolz',
            'Nobert',
            'Prof. Dr. Nobert Bolz',
        ),
    ),
])
def test_detector_parser_parse_person(raw, expected):
    parsed = parse(raw)
    assert parsed == expected, str(parsed)


def test_detector_parser_person_order_person():
    persons = [KAHN, GOMEZ, HELMUT]
    expected = (HELMUT, [GOMEZ, KAHN])
    current = order_persons(persons)

    assert current == expected, str(current)


def test_detector_parser_person_parse_person_without_title():
    raw = '  Vorgelegt von    Helmut Konrad Fahrendholz   '
    expected = iamraw.Person(
        title=Title.NO_TITLE,
        name='Fahrendholz',
        firstname='Helmut Konrad',
        raw=raw.strip(),
    )
    parsed = detector.parser.person.parser_person_without_title(raw)
    assert parsed == expected
