# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utila

import hey.fonts.store
import hey.textnavigator.navigator

TEXT = r"""
dimension: 595.28 841.89
pages:
- children:
  - - TextContainer
    - - "Steuerung und \xDCberwachung intelligenter\n"
      - "Geb\xE4udetechnik\n"
  - - TextContainer
    - - 'Masterarbeit

        '
  - - TextContainer
    - - 'zur Erlangung des akademischen Grades Bachelor of Science

        '
  - - TextContainer
    - - "an der Hochschule f\xFCr Technik und Wirtschaft Berlin,\n"
  - - TextContainer
    - - 'Fachbereich Wirtschaftswissenschaften II,

        '
  - - TextContainer
    - - 'Studiengang Angewandte Kunst

        '
  - - TextContainer
    - - "vorgelegt von B.Sc. Thomas Helmer\n"
      - 'Matrikelnummer: 161647

        '
  - - TextContainer
    - - "1. Betreuer: Prof. Dr. Carsten Semilon\n"
      - '2. Betreuer: Dr.-Ing. Dirk Contemporary

        '
  - - TextContainer
    - - 'Berlin, den 8. August 2015

        '
  page: 0
"""

TEXT_TITLE = 'Steuerung und \xDCberwachung intelligenter Geb\xE4udetechnik'

TEXT_POSITION = """
- content:
  - 0 125.59 171.91 468.72 225.97
  - 1 245.41 249.72 348.90 270.18
  - 2 111.26 289.59 483.06 309.78
  - 3 131.74 307.52 462.58 327.71
  - 4 169.28 325.46 425.03 345.65
  - 5 184.20 339.90 410.11 360.09
  - 6 102.88 526.24 242.76 557.51
  - 7 102.88 593.99 302.20 625.26
  - 8 102.88 661.73 225.79 678.55
  page: 0
"""

FONT_HEADER = """
- font:
    name: LMRoman17
    scale: 29.2
    weight: LIGHT
  index: 0
- font:
    name: LMRoman12
    scale: 20.5
    weight: BOLD
  index: 1
- font:
    name: LMRoman12
    scale: 20.2
    weight: LIGHT
  index: 2
- font:
    name: LMRoman12
    scale: 16.8
    weight: LIGHT
  index: 3
"""

FONT_CONTENT = """
- fonts:
  - 1 0 0 1233068222
  - 2 0 0 218355784
  - 6 0 0 -593951746
  - 8 0 24 -186368956
  page: 0
"""


def new_fontstore():
    fontstore = hey.fonts.store.create_fontstore(
        serializeraw.load_font_header(FONT_HEADER),
        serializeraw.load_font_content(FONT_CONTENT),
    )
    return fontstore


@pytest.fixture
def new_textnavgiator():
    navigators = hey.textnavigator.navigator.create_pagetextnavigators(
        serializeraw.load_document(TEXT, pages=0),  # just load the first page
        serializeraw.load_textpositions(TEXT_POSITION, pages=0),
    )
    first = utila.select_page(navigators, page=0)
    return first
