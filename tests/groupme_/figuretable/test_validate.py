# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw
import utila

import groupme.path
import tests.resources


def merge_required(toc: iamraw.Toc) -> str:
    result = []

    def recursive(item, level):
        result = []
        result.append('    ' * level + item.title)
        assert item.raw_location >= 0, str(item)
        if item.children:
            for child in item.children:
                result.extend(recursive(child, level + 1))
        return result

    for item in toc:
        result.extend(recursive(item, level=0))
    titles = utila.NEWLINE.join(result)
    return titles


FIGURETABLE_BACHELOR90 = """\
Verknüpfung klassisches und AUTOSAR-Steuergerät
linearer Bus und ein Einzelstern nach [WL11]
Pegel bei der NRZ-Datenübertragung
Nominelle Potentiale nach [WR10, Seite 214]
Buszugriff Abitrierungsphase nach [WR10, Seite 216]
CAN-Nachricht nach [WL11, Seite 19]
Generierung für abstrakte Schnittstelle nach [Rum05, Seite 61]
Parametrisierte Codegenerierung nach [Rum05, Seite 62]
Kapselung der Zugriffe nach [JL07, Seite 389]
Handgeschriebenes System
Zusammengesetztes System
Komplett integriertes System
Umsetzung des Treiberkonzepts in Simulink nach [mat12a]
S-Function Builder mit vier Eingangsports und einem Ausgangs- ports sowie ein S-Funktion-Block
Möglichkeiten des Testens nach [JL07, Seite 253]
Testfall durchführen nach [JL07, Seite 258]
Ablauf Regressionstest nach [Lig09, Seite 194]
MiL-Prinzip nach [Plu06, Seite 3]
SiL-Prinzip
Allgemeine Einordnung des Debuggings in den Testprozess nach [AT09, Abschnitt 8.2.3]
Drehgestell Sensorverteilung
Softwareentwicklung Übersicht
Allgemeiner Ablauf der Entwicklung
Allgemeiner Aufbau der Algorithmen
Allgemeiner Ablauf des Algorithmus
Nachrichtenformat
Deserialisierung der Nachrichten
Buffer Funktionsübersicht
Histogramm zur Durchmesserbestimmung
Einlesen vom Speicher
MiL-Test für das Histogramm
Manuelle Integration der Durchmesserberechnung
Integrationstest Einlesen
Manueller Test der Gesamtintegration
MiL-Test zum Histogramm
Integration Durchmesser
SiL- und HiL-Test auf der OBU und dem Entwicklungsrechner"""


def bachelor90(toc: iamraw.Toc):
    figures = merge_required(toc)
    assert figures == FIGURETABLE_BACHELOR90, figures


TEN = tuple(range(10))


@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(
        tests.resources.BACHELOR90,
        bachelor90,
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        id='bachelor90',
    ),
])
@utila.skip_longrun
def test_groupme_figuretable(source, validate, pages, monkeypatch, testdir):
    pages = ','.join((str(item) for item in pages)) if pages else ''
    pages = f'--pages={pages}' if pages else ''
    cmd = f'-i {source} --figuretable {pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    path = groupme.path.figuretable(testdir.tmpdir)
    figuretable = serializeraw.load_toc(path)
    validate(figuretable)
