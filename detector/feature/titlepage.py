# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""                         TITLE PAGE EXTRACTOR

The title page extractor extracts information like author, type of work,
university, date etc. out of the defined title page. Further `decision unit`s
gets these information and judge them if there are right or something is
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
import texmex
import utila

import detector.parser.complete
import detector.titlepage

# TODO: MOVE TO MORE GENERAL POSITION
# TODO: check 0.1, use a higher number?
RAWMAKER_CONFIGURATION = (
    '--prefix=oneline '
    '--font --text '
    '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001')

# Include first 5 pages into TitlePage detection
SELECTED_PAGES = (0, 1, 2, 3, 4)


def work(text: str, text_positions: str, pages: tuple = None) -> str:
    if pages is None:
        # first five pages
        pages = SELECTED_PAGES
    text = serializeraw.load_document(text, pages=pages)
    text_positions = serializeraw.load_textpositions(
        text_positions,
        pages=pages,
    )

    navigators = texmex.create_pagetextnavigators(
        text,
        text_positions,
    )

    parsed = parse_titlepages(navigators, pages)
    best = detector.titlepage.select_best(parsed)

    dumped = serializeraw.dump_titlepage(best)
    return dumped


def parse_titlepages(navigators: texmex.PageTextNavigators, pages=None):
    if not pages:
        pages = SELECTED_PAGES
    result = []
    for page in pages:
        navigator = utila.select_page(navigators, page=page)
        if navigator is None:
            # white page
            parsed = None
        else:
            parsed = detector.parser.complete.parse(navigator)
        result.append(parsed)
    return result
