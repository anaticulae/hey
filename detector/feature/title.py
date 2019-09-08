# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""                         TITLE PAGE EXTRACTOR

The title page extractor extract information like author, type of work,
university, date etc. out of the defined title page. Are further `decision
unit` get these information are jduge them if there are right or something is
missing. A further unit gives advices how to improve the `title` page.

workplan:
    title extractor -> judging unit -> adivice unit -> presentation layer
                                    | - - - - - - - -> presentation layer

Shortcuts:

    TPE - Title Page Extractor
    JU  - Judging Unit
    AU  - Advice unit
    PL  - Presentation layer

How does the `TPE` work:

Extract Strings
        Numbers
        Date

        FontSizes
        Boundings



Requirements - "Wissenschaftliches Arbeiten" - Manuel Rene Theisen:

   + Universitaets, Fakultaet, Institut, Seminar
   + Pruefungszeit, laufendes Semenster
   + Art: Thesis, Seminar, Bachelor, Master, Disteration
   + Thema
   + Namensangabe des Pruefers
   + Name, Vorname des Verfassers mit eventuellem akademischem Titel
   + Matrikelnummer
   + Studienadresse
   + Studiengang, Fachrichtung, (Semesterzahl?)
   + Termin der Abgabe/Einreichung


"""

import serializeraw
import utila

from detector.parser.complete import parse
from hey.textnavigator.navigator import create_pagetextnavigators
from hey.utils import select_page


def work(text: str, text_positions: str) -> str:
    text = serializeraw.load_document(text, pages=0)
    text_positions = serializeraw.load_textpositions(text_positions, pages=0)

    navigators = create_pagetextnavigators(text, text_positions)
    navigator = select_page(navigators, page=0)
    parsed = parse(navigator)

    dumped = serializeraw.dump_titlepage(parsed)
    return dumped


def name():
    return 'title'


def commandline():
    return utila.Flag(
        longcut=name(),
        message='extract all features from a title page',
    )
