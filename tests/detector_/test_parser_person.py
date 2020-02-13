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

import detector.parser.person

HELMUT = iamraw.Person(
    iamraw.AcademicTitle.BSC,
    'Fahrendholz',
    'Helmut Konrad',
    'B.Sc. Helmut Konrad Fahrendholz',
)

GOMEZ = iamraw.Person(
    iamraw.PROF_DR,
    'Gomez',
    'Fabian',
    'Hochschullehrer: Prof. Dr.-Ing. Fabian Gomez',
)

KAHN = iamraw.Person(
    iamraw.PROF_DR,
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
            iamraw.AcademicTitle.MASTER,
            'Zickler',
            'Andreas',
            'Betreuer VAI:Dipl. Ing. Andreas Zickler',
        ),
    ),
    (
        'Betreuer: Prof. Dr. Groeg Trichter  ',
        iamraw.Person(
            iamraw.PROF_DR,
            'Trichter',
            'Groeg',
            'Betreuer: Prof. Dr. Groeg Trichter',
        ),
    ),
    (
        'Hochschullehrer: Prof.-Dr.-Ing. Clemens Gühmann',
        iamraw.Person(
            iamraw.PROF_DR,
            'Gühmann',
            'Clemens',
            'Hochschullehrer: Prof.-Dr.-Ing. Clemens Gühmann',
        ),
    ),
    (
        '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        iamraw.Person(
            iamraw.AcademicTitle.DR,
            'Contemporary',
            'Dirk',
            '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        ),
    ),
    (
        'Erstgutachter: Prof. Dr. rer. biol. hum. Erwin Paulat',
        iamraw.Person(
            iamraw.PROF_DR,
            'Paulat',
            'Erwin',
            'Erstgutachter: Prof. Dr. rer. biol. hum. Erwin Paulat',
        ),
    ),
    (
        'Zweitgutachter: Prof. Dr. med. Dr.-Ing. Ronald Verbus-Trapp',
        iamraw.Person(
            iamraw.PROF_DR,
            'Verbus-Trapp',
            'Ronald',
            'Zweitgutachter: Prof. Dr. med. Dr.-Ing. Ronald Verbus-Trapp',
        ),
    ),
    (
        '   vorgelegt von   Thomas Helmer  ',
        iamraw.Person(
            iamraw.AcademicTitle.STUDENT,
            'Helmer',
            'Thomas',
            'vorgelegt von   Thomas Helmer',
        ),
    ),
    (
        '   Verfasserin: Tina Tomate  ',
        iamraw.Person(
            iamraw.AcademicTitle.STUDENT,
            'Tomate',
            'Tina',
            'Verfasserin: Tina Tomate',
        ),
    ),
    (
        'Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt',
        iamraw.Person(
            iamraw.AcademicTitle.MASTER,
            'Frühwirt',
            'Stephan',
            'Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt',
        ),
    ),
    (
        'Prof. Dr. Nobert Bolz',
        iamraw.Person(
            iamraw.PROF_DR,
            'Bolz',
            'Nobert',
            'Prof. Dr. Nobert Bolz',
        ),
    ),
    (
        'Zweitgutachter: M.A. Erwin Nolte',
        iamraw.Person(
            iamraw.AcademicTitle.MASTER,
            'Nolte',
            'Erwin',
            'Zweitgutachter: M.A. Erwin Nolte',
        ),
    ),
    (
        'Zweitprüfer: Peter Thomson',
        iamraw.Person(
            iamraw.AcademicTitle.EXAMINIER,
            'Thomson',
            'Peter',
            'Zweitprüfer: Peter Thomson',
        ),
    ),
])
def test_detector_parser_parse_person(raw, expected):
    parsed = detector.parser.person.parse(raw)
    assert parsed == expected, str(parsed)


def test_detector_parser_person_order_person():
    persons = [KAHN, GOMEZ, HELMUT]
    expected = (HELMUT, [GOMEZ, KAHN])
    current = detector.parser.person.order_persons(persons)

    assert current == expected, str(current)


def test_detector_parser_person_parse_person_without_title():
    raw = '  Vorgelegt von    Helmut Konrad Fahrendholz   '
    expected = iamraw.Person(
        title=iamraw.AcademicTitle.STUDENT,
        name='Fahrendholz',
        firstname='Helmut Konrad',
        raw=raw.strip(),
    )
    parsed = detector.parser.person.parse_person_without_title(raw)
    assert parsed == expected
