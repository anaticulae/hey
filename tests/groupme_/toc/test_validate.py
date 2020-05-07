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
        if item.children:
            for child in item.children:
                result.extend(recursive(child, level + 1))
        return result

    for item in toc:
        result.extend(recursive(item, level=0))
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
        Persönlichkeitsstörungen
        Therapeut-Klient-Beziehung
Wirksamkeit der Verhaltenstherapie
Untersuchte verhaltenstherapeutische Standardmethoden
    Psychoedukation
        Selbstbeobachtung
        Konsumtagebuch
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
        Interpretation der Ergebnisse der Konsumtagebücher anhand der quantitativen Auswertung durch statistische Daten
        Interpretation der Ergebnisse der Fragebögen anhand der qualitativen Auswertung durch die qualitative Inhaltsanalyse nach Mayring
Beantwortung der Forschungsfragen und Hypothesen sowie Fazit und weiterführende Fragen
Literatur- und Quellenverzeichnis
Abbildungs- und Tabellenverzeichnis
Anhang
Versicherung selbständiger Arbeit"""


def master99(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_MASTER99


# # TODO: USE FULL VALIDATION LATER
# # Dateisystem have no level and is therefore parsed at level 1 item
# # Dateisystem
# #     Konfiguration des Messsystems
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
    Hardware Entwurf
        MSP430 Mikrocontroller
        Spannungsversorgung
        Strommessschaltung
        Ein- und Ausgänge
        Benutzerschnittstelle
        Gehäuse
    Mikrocontrollerprogramm
        Leistungs- und Energiemessung
        UART
        SD Card
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


def homework50(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_HOMEWORK50


# TODO: PARSE Literaturverzeichnis NODES correctly
TITLE_BACHELOR111 = """\
Einführung
    Motivation und Zielsetzung
    Aufbau der Arbeit
Grundlagen
    Smartphones
        Google Android
        Apple iPhoneOS
        Weitere Mobilplattformen
        Zusammenfassung
    Drahtlose Kommunikationstechnologien
        Drahtlostechnologien für Mobilfunknetze
        Drahtlostechnologien für lokale Netzwerke (WLAN)
        Drahtlostechnologien für Nahbereichsnetzwerke (WPAN)
        Zusammenfassung
    Gebäudeautomation
        KNX/EIB
        Weitere Bus-Technologien zur Gebäudeautomation
    Beispiele für Anwendungen zum mobilen Zugriffa uf Gebäu- deautomationssysteme
    Zusammenfassung
Anforderungsanalyse
    Anwendungsumgebung
        Einsatzgebiet
        Rahmenbedingungen
    Systemanforderungen
    Analyse der Anwendungsfälle
        Szenario 1: Anwendung läuft im lokalen Netzwerk
        Szenario 2: Anwendung läuft nicht im lokalen Netzwerk oder ist inaktiv
Systementwurf
    Architektur
        Datenschicht
        Steuerungsschicht
        Präsentationsschicht
Implementierung
    iPhone-Anwendung zur Steuerung und Überwachung von KNX-Systemen
        Entwicklungsumgebung
        Projektstruktur
        Datenschicht
        Steuerungsschicht
        Präsentationsschicht
Evaluierung und Demonstration des Prototypen
    Evaluierung des Systems
        Modularität und Erweiterbarkeit
        Funktionalität und Benutzbarkeit
    Demonstration des Prototypen
        Anwendungsstart und Konfiguration eines Projektes
        Auswahl von Projekten und KNX-Gruppen
        Steuern und Überwachen von KNX-Geräten
Zusammenfassung und Ausblick
    Zusammenfassung
    Ausblick
Glossar
Literatur
    Literaturverzeichnis
    Internetquellen
    Bildquellen
Abbildungsverzeichnis
Listings
Tabellenverzeichnis
A
    Diagramme
        Flussdiagramme
        Flussdiagramm Gruppe steuern und überwachen
        Klassendiagramme
    Benutzerschnittstellen
        Entwürfe der iPhone-Anwendung
    Fotos
        Aufbau der KNX-Gebäudeinstallation"""


def bachelor111(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_BACHELOR111


# yapf:disable, format the list by hand
@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(tests.resources.HOMEWORK50, homework50, (3, 4), id='homework50'),
    pytest.param(tests.resources.MASTER89, master89, (1,), id='master89'),
    pytest.param(tests.resources.MASTER98, master98, (1,), id='master98'),
    pytest.param(tests.resources.MASTER99, master99, (2, 3), id='master99'),
    pytest.param(tests.resources.BACHELOR111, bachelor111, (1, 2, 3, 4), id='bachelor111',
                 marks=pytest.mark.xfail(reason='literaturverzeichnis sub notes')),
])  # yapf:enable
def test_groupme_toc_validate(source, validate, pages, monkeypatch, testdir):
    pages = ','.join((str(item) for item in pages))
    cmd = f'-i {source} --toc --pages={pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    path = groupme.path.toc(testdir.tmpdir)
    toc = serializeraw.load_toc(path)
    validate(toc)
