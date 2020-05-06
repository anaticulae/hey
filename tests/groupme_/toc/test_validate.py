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
    for item in toc:
        result.append(f'{item.title}')
        result.extend([f'    {it.title}' for it in item.children])
    titles = utila.NEWLINE.join(result)
    return titles


TITLE_MASTER98 = """\
Einleitung
Theoretische Grundlagen
    Von der mémoire collective zu den Lieux de mémoire
    Binationale Erinnerungsorte
    Das dialogische Erinnern von Aleida Assmann
    Erinnerungsorte im DaF-Landeskundeunterricht
Der Elysée-Vertrag – Ein deutsch-französischer Erinnerungsort
    Die Vorgeschichte
    Adenauer, de Gaulle und der Elysée-Vertrag
    Mythos Elysée-Vertrag
    Die Entwicklung des Elysée-Vertrags vom Ereignis zum Erinnerungsort
Didaktisierung
    Eignung des Elysée-Vertrags für den DaF-Landeskundeunterricht
    Zielgruppe und Sprachniveau
    Zielsetzungen
    Vorstellung der Materialien
Reflexion
    Reflexion der Themenwahl
    Reflexion der Zielgruppe
    Reflexion der inhaltlichen Lernziele
    Reflexion der sprachlichen Lernziele
    Reflexion der Methodik und des Materials
    Reflexion der kulturdidaktischen Lernziele
Fazit und Ausblick
Verzeichnisse
    Literaturverzeichnis
    Tabellenverzeichnis
Anhang"""


def master98(toc: iamraw.Toc):
    # TODO: REPLACE DUE LEN AFTER UPGRADE
    assert len([item for item in toc]) == 8
    # titles = utila.NEWLINE.join([item.title for item in toc])
    titles = merge_required(toc)
    assert titles == TITLE_MASTER98, toc


TITLE_MASTER89 = """\
Einleitung
Sänger der Gegenwart: A Audiovisuelle Medien im Zeichen formaler Kontinuität
    Mediale Darstellung zwischen Mündlichkeit und Schriftlichkeit
    Mythos als Konstante audiovisuellen Erzählens
Lernen durch Geschichten: m Mythen und Spielfilme als Enzyklopädien des sozialen Verhaltens
    Wissen als soziales Konstrukt
    Mediale Wirklichkeit und Beobachtung von Verhalten
    Sinnliches Erleben und Wissenserwerb
Rhapsoden, Film und Fernsehen als Archivare sozialen Wissens
    Träger des kollektiven Gedächtnisses
    Mythos als sinnstiftende Organisationsform
Schlussbetrachtung und Ausblick
Literaturverzeichnis
Die Reise des Helden in der Odyssee
Die Reise des Helden in MATCH POINT
Die Reise des Helden in VINCENT WILL MEER"""


def master89(toc: iamraw.Toc):
    """This example contains 2 Errors. There is content which is hidden
    out of page border the `A` and `m` which follows out of bad
    formattting."""
    titles = merge_required(toc)
    assert titles == TITLE_MASTER89


TITLE_MASTER99 = """\
Abkürzungsverzeichnis
Einleitung
    Forschungskontext
    Persönliche Motivation
    Aufgabenstellung und Zielsetzung
    Aufbau der Arbeit
Betreuung und Klientel
    Betreutes Wohnen bei der ADV gGmbH
    Klientel
Wirksamkeit der Verhaltenstherapie
Untersuchte verhaltenstherapeutische Standardmethoden
    Psychoedukation
    Kontingenzmanagement
Forschungsfragen und Hypothesen
Forschungsplan
    Methode
    Beteiligter Personenkreis
    Rahmenbedingungen
    Testphase
    Einbringen ins Team und Intervention
Datenauswertung
    Mixed-Methods-Studie
    Quantitative Sozialforschung
    Qualitative Sozialforschung
    Interpretation der Ergebnisse
Beantwortung der Forschungsfragen und Hypothesen sowie Fazit und weiterführende Fragen
Literatur- und Quellenverzeichnis
Abbildungs- und Tabellenverzeichnis
Anhang
Versicherung selbständiger Arbeit"""


def master99(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_MASTER99


TITLE_HOMEWORK50 = """\
Abbildungsverzeichnis
Abkürzungsverzeichnis
Einleitung
Konzept
    Leistungs- und Energiemessung
    Aufbau
    UART Modus
    SD Card Modus
    Verarbeitung auf Host-System
Implementierung
    Hardwareentwurf
        MSP430 Mikrocontroller
        Spannungsversorgung
        Strommessschaltung
        Ein- und Ausgänge
        Benutzerschnittstelle
        Gehäuse
    Mikrocontrollerprogramm
        Leistungs- und Energiemessung
        UART
        SD CARD
            Dateisystem
        Konfiguration des Messsystems
        Auswertungs-/Empfängerprogramm
Benutzungshinweise
    Auswahl des Shuntwiderstands
    Auswahl der Abtastrate
    Verbinden der Messleitungen
    Messung
    Auswertung
Beispielmessung an Temperaturlogger
Verbesserungsmöglichkeiten
Zusammenfassung
Anhang"""

# TODO: USE FULL VALIDATION LATER
TITLE_HOMEWORK50 = """\
Abbildungsverzeichnis
Abkürzungsverzeichnis
Einleitung
Konzept
    Leistungs- und Energiemessung
    Aufbau
    UART Modus
    SD Card Modus
    Verarbeitung auf Host-System
Implementierung
    Hardwareentwurf
    Mikrocontrollerprogramm
Benutzungshinweise
    Auswahl des Shuntwiderstands
    Auswahl der Abtastrate
    Verbinden der Messleitungen
    Messung
    Auswertung
Beispielmessung an Temperaturlogger
Verbesserungsmöglichkeiten
Zusammenfassung
Anhang"""


def homework50(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_HOMEWORK50


# yapf:disable, format the list by hand
@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(tests.resources.HOMEWORK50, homework50, (3, 4), id='homework50', marks=pytest.mark.xfail(reason='improve')),
    pytest.param(tests.resources.MASTER89, master89, (1,), id='master89'),
    pytest.param(tests.resources.MASTER98, master98, (1,), id='master98'),
    pytest.param(tests.resources.MASTER99, master99, (2, 3), id='master99'),
])  # yapf:enable
def test_groupme_toc_validate(source, validate, pages, monkeypatch, testdir):
    pages = ','.join((str(item) for item in pages))
    cmd = f'-i {source} --toc --pages={pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    path = groupme.path.toc(testdir.tmpdir)
    toc = serializeraw.load_toc(path)
    validate(toc)
