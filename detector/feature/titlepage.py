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

import detector.parser.complete
import hey.textnavigator.navigator as htn

# TODO: MOVE TO MORE GENERAL POSITION
# TODO: check 0.1, use a higher number?
RAWMAKER_CONFIGURATION = ('--prefix=oneline '
                          '--font --text --toc '
                          '--boxes_flow=1.0 '
                          '--char_margin=100.0 '
                          '--line_margin=0.1')

# Include first 5 pages into TitlePage detection
SELECTED_PAGES = tuple(range(5))  # TODO: HOLY VALUE


def work(text: str, text_positions: str) -> str:
    text = serializeraw.load_document(text, pages=SELECTED_PAGES)
    text_positions = serializeraw.load_textpositions(
        text_positions,
        pages=SELECTED_PAGES,
    )

    navigators = htn.create_pagetextnavigators(
        text,
        text_positions,
    )

    parsed = parse_titlepages(navigators)
    import detector.titlepage  # TODO: MOVE TO PACKAGE LATER
    best = detector.titlepage.select_best(parsed)

    dumped = serializeraw.dump_titlepage(best)
    return dumped


def parse_titlepages(
        navigators: htn.PageTextNavigators,
        selected=SELECTED_PAGES,
):
    result = []
    for index in selected:
        navigator = utila.select_page(navigators, page=index)
        if navigator is None:
            # white page
            parsed = None
        else:
            parsed = detector.parser.complete.parse(navigator)
        result.append(parsed)
    return result


def name():
    return 'titlepage'


def commandline():
    return utila.Flag(
        longcut=name(),
        message='extract all features from a title page',
    )
