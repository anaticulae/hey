# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import approx
from pytest import fixture

from sections.feature.toc import extract_toc_likelihood
from sections.feature.toc import work
from tests.resources import RESTRUCT_ONELINE_TEXT
from tests.sections_ import restructured_document  # pylint:disable=W0611


#pylint:disable=W0621
def test_extract_toc_likelihood(restructured_document):
    extracted = extract_toc_likelihood(restructured_document)
    assert sum(extracted) == approx(1.0)


@fixture
def restructured_toc():
    result = work(RESTRUCT_ONELINE_TEXT)
    return result
