# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest

import tests.groupme_.figuretable


@pytest.mark.parametrize('source,  pages', [
    pytest.param(
        power.link(power.MASTER089_PDF),
        (85, 86, 87, 88),
        id='master89_page85_86_87_88',
    ),
])
def test_regression_non_valid_examples(source, pages, monkeypatch, testdir):
    extracted = tests.groupme_.figuretable.extract_figuretable(
        source,
        pages,
        monkeypatch,
        testdir,
    )
    assert not extracted
