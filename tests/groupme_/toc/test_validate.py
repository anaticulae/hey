# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

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


TITLE_MASTER83 = """\
Einleitung
Definition: Protest und soziale Bewegung
Luhmanns „Theorie sozialer Systeme“
    Die Unterscheidung von System und Umwelt
    Soziale Systeme
    Die funktionale Differenzierung der Gesellschaft
        Was ist Gesellschaft?
        Folgeprobleme funktionaler Differenzierung
    Soziale Bewegungen und die Systemtheorie
        Funktionen sozialer Bewegungen
        Soziale Bewegungen als Systeme
        Öffentlicher Druck mithilfe der Massenmedien
    Das System der Massenmedien
„Don’t hate the media…“: Protestkommunikation und die Massenmedien
    Strukturelle Kopplung
    Protestkommunikation und die Massenmedien
    Framing
    Protestkommunikation und die Selektoren
    Die expressive Funktion von Protest
    Kritik oder: Gründe, die Massenmedien zu „hassen“
„…become the media“ – Protestkommunikation und das Internet
    Was ist das Internet?
    Mehr Demokratie durch das Internet?
    Die „Wahlverwandtschaft“
    Neue Möglichkeiten
        Information
        Interaktive Kommunikation
        Ein Beispiel: Indymedia
    Das „Mediendispositiv Internet“ oder: Gibt es eine internetspezifische Protestkommunikation?
        Intern und extern
        Connective action
        Eine neue Form von Protestkommunikation
    Protestkommunikation zwischen Massenmedien und Internet
Fazit
Literaturverzeichnis"""


def master83(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_MASTER83, titles


TITLE_BACHELOR241 = """\
Eidesstattliche Erklärung
Danksagung
Einleitung
Studiendesign
    Zeitlicher Verlauf der SOLAR-Kohortenstudie
    Basiserhebung: ISAAC II
    1. Follow-up: SOLAR I
    2. Follow-up: SOLAR II
    Tätigkeitskodierung und Job-Exposure-Matrix
Fehlende Daten
    Fehlendmechanismen und grundlegende Begriffe
    Umgang mit fehlenden Daten
        Methoden für Betrachtung der beobachteten Werte
        Imputationsmethoden - Ersetzen der fehlenden Werte
        Kombination der Schätzer
Datenmanagement
    Datengrundlage
    Datenbereinigung
        Korrekturen der Tätigkeitsdaten
    Auswahl der Probanden mit vollständigen Tätigkeitsangaben
Imputation der fehlenden Werte in den potentiellen Confoundervariablen
    Imputation durch Ziehen gemäß der Randverteilung der Daten
        Binäre Variablen
        Kategoriale Variablen
    Imputation mithilfe des R-Packages AMELIA II
        Allgemeines
        Wie funktioniert AMELIA II ?
        Transformation von Variablen
        Identifkiationsvariablen
        Auswahl der Variablen bei der Imputation
        Behandlung von Variablen mit hohen Korrelationen
    Übersicht über die Variablenausprägungen in den imputierten Datensätzen
Berechnung der Expositionsvariablen
    Komplexe Matrix als Basis für alle Expositionsberechnungen
    Berechnung der Exposition kumuliert über alle Tätigkeiten und Jahre
    Berechnung der Exposition in der ersten ausgeübten Tätigkeit
    Berechnung der Exposition im ersten Tätigkeitsjahr
    Betrachtung der gebildeten Expositionsvariablen
Logistische Regression
    Modellannahmen
    Parameterschätzung
    Parameterinterpretation
    Likelihood-Quotienten-Test
    Variablenselektion und Modellwahl: AIC-Kriterium
    GAM (Generalized Additive Model)
    ROC-Analyse
    Logistische Regressionsmodelle für die Probanden mit vollständigen Tä- tigkeitsdaten
        Mögliche Einflussgrößen (“Confounder”) für die logistischen Modelle
        Variablenselektion und Modellwahl
        ROC-Analyse für die “besten” Modelle
        Schätzer kombinieren
        Interpretation der Odds-Ratios der kombinierten Parameterschützer
        Diskussion der logistischen Regressionsmodelle
Simulation
    Erzeugen eines Fehlendmusters in den Tätigkeitsdaten
    Imputation der fehlenden Werte in den Tätigkeitsdaten
        Vorgehen bei der Imputation
        Imputation der Zeitangaben
        Imputation der Wochenstunden
    Logistische Regressionsmodelle auf imputierten Tätigkeitsdaten
    Vergleich der Parameterschützer
Zusammenfassung und Ausblick
    Zusammenfassung
    Ausblick
A Variablenkodierung
    Variablen aus ISAAC II
        In Deutschland geboren
        Atopie der Eltern
        Kind gestillt
        Neurodermitis
        Allergische Rhinitis
        Asthma
        Passivrauch
        Soziökonomischer Status
        Studienzentrum
        Geschwister
    Variablen aus SOLAR I
        Rauchverhalten
        Berufssituation
    Variablen aus SOLAR II
        Asthma
        Allergische Rhinitis
        Rauchverhalten
        Berufssituation
        Schulbildung
    Benötigte Variablen für die Tätigkeitsdaten
        Gearbeitet in SOLAR I
        Gearbeitet in SOLAR II
A
Anzahl der Wochenstunden)
    Ende der Tätigkeit in SOLAR-I
    Ende der Tätigkeit in SOLAR II
A
SOLAR II
    Anzahl Tätigkeitsangaben in SOLAR I und SOLAR II
    Dauer der Tätigkeit
    Zeilen mit vollständig ausgefüllten Tätigkeitsangaben
    Probanden mit vollständig ausgefüllten Tätigkeitsangaben
    Benötigte Variable für die Simulation
    Benötigte Variablen für die Job-Matrix
A
A
B Alle Abbildungen zum Vergleich der Parameterschätzer
C R-Code
    Imputation der fehlenden Werte in den potentiellen Confoundervariablen
        Imputation durch Ziehen gemäß der Randverteilung der Daten
        Imputation mithilfe des R-Packages AMELIA II
    Berechnung der Expositionsvariablen
    Logistische Regression
        Schritt 1 - Confoundermodell
        Schritt 2 - Modelltest
        Schritt 3 - GAM
        Schritt 4 - Expositionsvariablen
        Schritt 5 - Bestes Modell
        Schritt 6 - Schützer kombinieren
    Simulation
        Schritt 1 - Werte künstlich löschen
        Schritt 2 - Imputation der fehlenden Werte in den Tätigkeitsdaten
D CD Inhalt"""


def bachelor241(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_BACHELOR241, titles


TITLE_BACHELOR76 = """\
Abkürzungsverzeichnis
Abbildungsverzeichnis
Tabellenverzeichnis
Einleitung
    Problemstellung
    Zielsetzung und Forschungsleitfragen
    Methodische Vorgehensweise
    Aufbau und Struktur der Arbeit
Theoretische Grundlagen
    Treiber der Digitalisierung und Begriffsbestimmung
    Historische Entwicklung zur vierten industriellen Revolution
    Herkunft und Definition des Begriffs Industrie 4.0
    Abgrenzung und Definition des Mittelstandsbegriffs
Bausteine der digitalen Infrastruktur zur Befähigung von Industrie 4.0
    Cyber-Physische-Systeme in der Industrie 4.0
        Ubiquitous Computing
        Internet der Dinge und Dienste
        Cloud Computing
    Big Data und Analytics-Dienste in der Industrie 4.0
    Mensch-Maschine-Interaktion in der Industrie 4.0
Auswirkungen der Digitalisierung und Industrie 4.0 entlang der Wertschöpfungskette
    Primäraktivitäten der Wertschöpfungskette
        Produktion
        Logistik
        Marketing und Vertrieb
        Services
    Unterstützungsaktivitäten der Wertschöpfungskette
        Innovation und Transformation
        Vernetzung und Kooperation
        Daten und Analytik
        Organisation der Arbeit
Schlussbetrachtung und Ausblick
Literatur- und Quellenverzeichnis
Eidesstattliche Erklärung
Anhang"""


def bachelor76(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_BACHELOR76, titles


TITLE_MASTER72 = """\
Einleitung
    Fragestellung und Zielsetzung
    Aufbau der Arbeit
Das Social Web und die Privatsphäre – Selbstdarstellungsverhalten der Nutzer aus Sicht von Massenmedien und Literatur
    Web 2.0, Social Web und Social Media: Abgrenzungen und Definitionen
    Merkmale von Social Network Sites
    Eigenschaften netzbasierter Kommunikation
    Einführung in das Konzept der Privatheit
    Darstellungen in Massenmedien und Literatur
        Selbstdarstellung und Privatheit als Problemfelder
        Mögliche Gründe für die Freizügigkeit im Umgang mit privaten Daten
        Privacy Paradox und Post-Privacy
Systemtheorie und moderne Netzwerksoziologie – zentrale Ansätze und Begriffe für den Themenkomplex Social Media
    Öffentlichkeit aus systemtheoretischer Sicht
    Interaktion als soziales System
    Personenbegriff nach Luhmann
    Erwartungen
    Vertrauen
    Identitätsbildung nach der modernen Netzwerksoziologie
        Identitäten suchen Kontrolle
        Identitätsdimensionen
        Soziale Netzwerke beinhalten Stories
    Abschließende Bemerkungen zur Vereinbarkeit beider Theorien
Privatheit und Identitätsbildung im Social Web – funktional betrachtet
    Social Media als Interaktionsräume
    Kontextbildung und Empfängerdifferenzierung im Social Web
    Potenzielle Öffentlichkeit
    Social Media contra Öffentlichkeit
    Identitätsbildung im Social Web
Schlussbetrachtung und Fazit
Literaturverzeichnis
Eidesstattliche Erklärung"""


def master72(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_MASTER72, titles


TITLE_BACHELOR90 = """\
Abbildungsverzeichnis
Tabellenverzeichnis
Abkürzungsverzeichnis
Einleitung
    Motivation
    Zielsetzung und Aufbau der Arbeit
Grundlagen eingebetteter Systeme
    Embedded System
        Systembegriff
        Computersysteme
        Entwicklungen im Embedded-Bereich
    Standards in der eingebetteten Softwareentwicklung
        AUTOSAR
        MISRA-C
    Controller Area Network - CAN
        Topologie
        Datenübertragung
Methodik
    Modellgetriebene Softwareentwicklung
        Entwicklungswerkzeuge
        Stand der Technik im Automobilbereich
    Automatische Codegenerierung aus Modellen
        Konzept
        Probleme beim Erzeugen von Quellcode
        Validierung der Ergebnisse
    Strategien zur Zerlegung der Probleme
        Randbedingungen
        Modularisierung
        Information Hiding
        Kopplung
    Umsetzung des Softwaresystems
        Manuell erzeugter Quellcode
        Modulweise Automatisierung, manuelle Verknüpfung
        Vollständige Automatisierung
        Zusammenfassung der Umsetzung
    Simulink
        Embedded Coder
        Verwendung von S-Funktionen
        Erzeugen des Simulinkmodells
    Testen der Software
        Softwarespezifikation
        Grundprinzip der Prüfung
        Klassifikation der Tests nach Komplexität
        Testen eingebetteter Systeme
        Bewertung des Testens als Prüfverfahren
    Debugging der Software
    Eignung für die Umsetzung
Umsetzung
    Problemstellung
    Vorgehen um Code zu erzeugen
    Übersicht der praktischen Entwicklung
        Entwicklungsumgebung Ubuntu
        Arbeit auf der OBU
    Allgemeiner Aufbau der Algorithmen
    Umsetzung der Algorithmen
        Algorithmus zur Durchmesserberechnung
        Moduldefinition
    Komponententest
        Testen der Komponente Einlesen
        Testen des Buffers
        Testen der Durchmesserberechnung
        Verifikation des Histogramms
    Integration und Integrationstest der entwickelten Komponenten
        Manuelle Integration
        Vollständige Integration in Simulink
        Bewertung
Diskussion und Ausblick
Anhang
    Konfiguration
        Software
        OBU
    Befehlsreferenz
    Verzeichnisübersicht Ubuntu
    Verzeichnisübersicht OBU
    Umsetzung
        Konfiguration der Modelle
        S-Funktion erzeugen
        S-Funktion einbinden
        Konfiguration Mex
    Testergebnisse"""


def bachelor90(toc: iamraw.Toc):
    titles = merge_required(toc)
    assert titles == TITLE_BACHELOR90, titles


TEN = tuple(range(10))


# yapf:disable, format the list by hand
@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(power.link(power.BACHELOR076_PDF), bachelor76, TEN, id='bachelor76'),
    pytest.param(power.link(power.BACHELOR111_PDF), bachelor111, (1, 2, 3, 4), id='bachelor111',
                 marks=pytest.mark.xfail(reason='literaturverzeichnis sub notes')),
    pytest.param(power.link(power.BACHELOR241_PDF), bachelor241, (4, 5, 6, 7), id='bachelor241',
                 marks=pytest.mark.xfail(reason='literaturverzeichnis sub notes')),
    pytest.param(power.link(power.HOMEWORK050_PDF), homework50, (3, 4), id='homework50'),
    pytest.param(power.link(power.MASTER083_PDF), master83, TEN, id='master83'),
    pytest.param(power.link(power.MASTER089_PDF), master89, TEN, id='master89'),
    pytest.param(power.link(power.MASTER098_PDF), master98, TEN, id='master98'),
    pytest.param(power.link(power.MASTER099_PDF), master99, TEN, id='master99'),
    pytest.param(power.link(power.MASTER072_PDF), master72, None, id='master72'),
    pytest.param(power.link(power.BACHELOR090_PDF), bachelor90, (4, 5, 6), id='bachelor90'),
])  # yapf:enable
@utilatest.skip_nightly
def test_groupme_toc_validate(source, validate, pages, monkeypatch, testdir):
    """Verify parsing behavior and check that toc is located
    automatically in range of `TEN` pages."""
    pages = ','.join((str(item) for item in pages)) if pages else ''
    pages = f'--pages={pages}' if pages else ''
    cmd = f'-i {source} --toc {pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    path = groupme.path.toc(testdir.tmpdir)
    toc = serializeraw.load_toc(path)
    validate(toc)
