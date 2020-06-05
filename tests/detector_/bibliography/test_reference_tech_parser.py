# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import detector.bibliography.reference.tech as dbrt

CONTENT = """\
Verknüpfung klassisches und AUTOSAR-Steuergerät
linearer Bus und ein Einzelstern nach [WL11]
Pegel bei der NRZ-Datenübertragung
Nominelle Potentiale nach [WR10, Seite 214]
Buszugriff Abitrierungsphase nach [WR10, Seite 216]
CAN-Nachricht nach [WL11, Seite 19]
Codegenerierung nach [Rum05, Seite 62]
der Zugriffe nach [JL07, Seite 389]
[VAC+08]
[mat12b]
[Sch05, Seite 3-4]
[ Ju04] JUERGEN LEOHOLD:
"""


def test_parse_tech():
    extracted = dbrt.parses(CONTENT)
    assert len(extracted) == 10
