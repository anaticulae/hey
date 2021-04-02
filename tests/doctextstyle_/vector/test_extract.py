# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import doctextstyle

FIRST_LEVEL = """\
KAPITEL 1: EINLEITUNG
KAPITEL 2: BEGRIFFSKLÄRUNG UND EIGNUNGSDIMENSIONEN VON BETEILIGUNGSINSTRUMENTEN
KAPITEL 3: STRATEGIEN DER EUROPÄISCHEN KOMMISSION ZUR PARTIZIPATION DER ZIVILGESELLSCHAFT
KAPITEL 4: FALLSTUDIE - DIE BETEILIGUNG DER ZIVILGESELLSCHAFT AM BEISPIEL DES HÄRTEFALLS BERLIN- NEUKÖLLN
KAPITEL 5: FÜR EINE BÜRGERNAHE UND DEMOKRATISCH LEGITIMIERTE EUROPÄISCHE POLITIK ZUR BETEILIGUNG DER ZIVILGESELLSCHAFT
"""

SECOND_LEVEL = """\
1.1. VOM EUROPÄISCHEN BINNENMARKT ZUM EUROPA DER BÜRGER
1.2. FORSCHUNGSDESIGN
1.3. AUFBAU DER ARBEIT
2.1. BEGRIFFSKLÄRUNG
2.2. TYPOLOGISIERUNG VON BETEILIGUNGSINSTRUMENTEN
2.3. EIGNUNGSDIMENSIONEN VON BETEILIGUNGSINSTRUMENTEN
2.4. ANALYSERASTER
3.1. DER STRATEGISCHE ENTWICKLUNGSPROZESS IM CHRONOLOGISCHEN VERLAUF
3.2. BEWERTUNG UND ANALYSE DES STRATEGIEWANDELS
4.1. DARSTELLUNG UND BEGRÜNDUNG DER FALLAUSWAHL
4.2. PROBLEMLAGENBESCHREIBUNG
4.3. POTENZIALBESCHREIBUNG
4.4. DER UNTERSUCHUNGSANSATZ
4.5. DIE EIGNUNG DER BETEILIGUNGSINSTRUMENTE DER EU - KOMMISSION IN BERLIN- NEUKÖLLN
4.6. ZWISCHENFAZIT
5.1. ZUSAMMENFASSUNG DER ERGEBNISSE UND SCHLUSSFOLGERUNGEN
5.2. KÜNFTIGE HERAUSFORDERUNGEN
5.3. LÖSUNGS- UND GESTALTUNGSANSÄTZE
"""


def headlines_raw(items: str) -> str:
    items = [utila.normalize_whitespaces(item.text.strip()) for item in items]
    # add final newline
    items = items + ['']
    result = utila.NEWLINE.join(items)
    return result


@utilatest.nightly
def test_vector_diss266_extract():
    source = power.link(power.DISS266_PDF)
    pages = utila.ranged_tuple(7, 215)
    headlines = doctextstyle.extract_headlines(source, pages)
    assert len(headlines) == 4
    first, second, third, fourth = headlines  # pylint:disable=W0612,W0632
    # first level
    assert len(first) == 5  # VALIDATED
    assert headlines_raw(first) == FIRST_LEVEL
    # second level
    assert len(second) == 18  # VALIDATED
    assert headlines_raw(second) == SECOND_LEVEL
