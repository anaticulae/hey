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


def master78(toc: iamraw.Toc):
    for item in toc:
        print(item.title)


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
    result = []
    for item in toc:
        result.append(f'{item.title}')
        result.extend([f'   {it.title}' for it in item.children])
    titles = utila.NEWLINE.join(result)
    # titles = utila.NEWLINE.join([item.title for item in toc])
    assert titles == TITLE_MASTER98, toc


@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(tests.resources.MASTER78, master78, (2, 3, 4), id='master78'),
    pytest.param(tests.resources.MASTER98, master98, (1,), id='master98'),
])
def test_groupme_toc_validate(source, validate, pages, monkeypatch, testdir):
    pages = ','.join((str(item) for item in pages))
    cmd = f'-i {source} --toc --pages={pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    path = groupme.path.toc(testdir.tmpdir)
    toc = serializeraw.load_toc(path)
    validate(toc)
