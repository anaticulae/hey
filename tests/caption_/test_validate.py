# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import utila

import tests.caption_.utils

BACHELOR56_TABLE = """\
Tabelle 1: Versuchsplan

Tabelle 2: Korrelation nach Pearson (Kreuzung)

Tabelle 3: Ergebnisse der Regressionsanalyse Geschwindigkeit und Bremsreaktionszeit mit der abhängigen Variable Unfall Kreuzung.

Tabelle 4: Korrelation nach Pearson (Fußgänger)

Tabelle 5: Ergebnisse der Regressionsanalyse Geschwindigkeit und Bremsreaktionszeit mit der abhängigen Variable Unfall FG.
"""


@pytest.mark.xfail(reason='improve table parser')
@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR056_PDF, BACHELOR56_TABLE, id='bachelor56'),
])
def test_validate_caption_table(source, expected, testdir, monkeypatch):
    """In the current state, the table is not parsed correctly. Table
    one is parsed too small. After improving the table parser, labels
    will be parsed better."""
    extracted = tests.caption_.utils.extract_captions(
        source,
        ':',
        testdir,
        monkeypatch,
        resultpath=iamraw.path.table_caption,
        selected='--table',
    )
    extracted = utila.flatten(page.content for page in extracted)
    extracted = [caption.raw for caption in extracted]
    extracted = (utila.NEWLINE * 2).join(extracted)  # pylint:disable=R0204
    assert extracted == expected
