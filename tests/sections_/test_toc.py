# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import approx

from sections.feature.toc import extract_toc_likelihood
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_text


#pylint:disable=W0621
def test_extract_toc_likelihood(restructured_text):
    extracted = extract_toc_likelihood(restructured_text)
    extracted = [item.content.value for item in extracted]
    assert sum(extracted) == approx(1.0)
