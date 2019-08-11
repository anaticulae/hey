# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from detector.parser.complete import TitlePage
from detector.parser.date import TitleDate
from detector.parser.institution import Institution
from detector.parser.matrikel import Matrikel
from detector.parser.person import PROF_DR
from detector.parser.person import Person
from detector.parser.person import Title
from detector.parser.thesis import DocumentType
from detector.parser.thesis import TitleThesisType

FIRST = """
Faktultät IV
Institut für gute Getränke

Modellierung und Simulation eines hybriden Lokomotivantriebs

Masterarbeit

vorgelegt von:

B.Sc. Helmut Konrad Fahrendholz 321240

Hochschullehrer: Prof. Dr.-Ing. Cuba Libre
Zweitgutachter: Prof. Dr.-Ing. Coffee Lover
Betreuer: Dipl. Ing. Thomas MÜller

Technische Universität Berlin, Fakultät IV, Institut für gute Getränke,
Fachgebiet Trinken und Essen,

Berlin, 19. April 2016
"""

FIRST_INSTITUTION = Institution(
    courseofstudies=None,
    department='IV',
    field='Trinken und Essen',
    institute='für gute Getränke',
    university='Technische Universität Berlin',
)
FIRST_EXPECTED = TitlePage(
    # title='Modellierung und Simulation eines hybriden Lokomotivantriebs',
    thesis=TitleThesisType(DocumentType.MASTER, 'Masterarbeit', 'Masterarbeit'),
    date=TitleDate(2016, 4, 19, 'Berlin', True, 'Berlin, 19. April 2016'),
    author=Person(
        Title.BSC,
        'Fahrendholz',
        'Helmut Konrad',
        'B.Sc. Helmut Konrad Fahrendholz',
    ),
    matrikel=Matrikel(321240, '', '321240'),
    examiner=[
        Person(
            Title.MASTER,
            'MÜller',
            'Thomas',
            'Betreuer: Dipl. Ing. Thomas MÜller',
        ),
        Person(
            Title.PROF | Title.DR,
            'Libre',
            'Cuba',
            'Hochschullehrer: Prof. Dr.-Ing. Cuba Libre',
        ),
        Person(
            Title.PROF | Title.DR,
            'Lover',
            'Coffee',
            'Zweitgutachter: Prof. Dr.-Ing. Coffee Lover',
        ),
    ],
    institution=FIRST_INSTITUTION,
)

SECOND = """
Steuerung und Überwachung intelligenter Gebäudetechnik

Masterarbeit

zur Erlangung des akademischen Grades Master of Science
an der Hochschule für Technik und Wirtschaft Berlin,
Fachbereich Wirtschaftswissenschaften II,
Studiengang Angewandte Kunst

vorgelegt von B.Sc. Thomas Helmer
Matrikelnummer: 161647

1. Betreuer: Prof. Dr. Carsten Semilov
2. Betreuer: Dr.-Ing. Dirk Contemporary

Berlin, den 8. August 2015
"""

SECOND_INSTITUTION = Institution(
    university='Hochschule für Technik und Wirtschaft Berlin',
    field='Wirtschaftswissenschaften II',
    courseofstudies='Angewandte Kunst',
)
SECOND_EXPECTED = TitlePage(
    # title='Steuerung und Überwachung intelligenter Gebäudetechnik',
    thesis=TitleThesisType(DocumentType.MASTER, 'Masterarbeit', 'Masterarbeit'),
    date=TitleDate(2015, 8, 8, 'Berlin', True, 'Berlin, den 8. August 2015'),
    author=Person(
        Title.BSC,
        'Helmer',
        'Thomas',
        'vorgelegt von B.Sc. Thomas Helmer',
    ),
    matrikel=Matrikel(161647, 'Matrikelnummer:', 'Matrikelnummer: 161647'),
    examiner=[
        Person(
            Title.DR,
            'Contemporary',
            'Dirk',
            '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        ),
        Person(
            PROF_DR,
            'Semilov',
            'Carsten',
            '1. Betreuer: Prof. Dr. Carsten Semilov',
        ),
    ],
    institution=SECOND_INSTITUTION,
)
