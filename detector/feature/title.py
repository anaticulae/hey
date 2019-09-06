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
from typing import Tuple

from utila import Flag


def work(infile: str) -> Tuple[str, str]:
    pass


def name():
    return 'title'


def commandline():
    return Flag(
        longcut=name(),
        message='extract all features from a title page',
    )
