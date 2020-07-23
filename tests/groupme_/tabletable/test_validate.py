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
import tests.groupme_


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


# TODO: IMPROVE PARSER A.10 and A.11 is not fully correct
TABLETABLE_BACHELOR90 = """\
Konfiguration Simulink Modell
Konfiguration Putty
Konfiguration WinSCP-Login
Anschlussbelegung OBU
PTX-Befehlsreferenz
Verzeichnisübersicht - Ubuntu
Verzeichnisübersicht - OBU
Vorgehen Konfiguration SIMULINK-Modell
Vorgehen zur Erzeugung einer S-Funktion
A.10.Vorgehen zum Einbinden von S-Funktionen
A.11.Datentypen Ports Mex nach [mat12b]"""


def bachelor90(toc: iamraw.Toc):
    tables = merge_required(toc)
    assert tables == TABLETABLE_BACHELOR90, tables


@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(
        power.link(power.BACHELOR090_PDF),
        bachelor90,
        (9, 10),
        id='bachelor90',
    ),
])
@utilatest.skip_longrun
def test_groupme_tabletable(source, validate, pages, monkeypatch, testdir):
    pages = ','.join((str(item) for item in pages)) if pages else ''
    pages = f'--pages={pages}' if pages else ''
    cmd = f'-i {source} --tabletable {pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    path = groupme.path.tabletable(testdir.tmpdir)
    tabletable = serializeraw.load_toc(path)
    validate(tabletable)
