# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import pytest
import serializeraw

import sections.feature.toc
import tests.resources
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_text


#pylint:disable=W0621
def test_extract_toc_likelihood(restructured_text):
    extracted = sections.feature.toc.extract_toc_likelihood(restructured_text)
    extracted = [item.content.value for item in extracted]
    assert sum(extracted) == pytest.approx(1.0)


def test_extract_toc_likelihood_bachelor63():
    text = iamraw.path.text(tests.resources.BACHELOR63, prefix='oneline')
    text = serializeraw.load_document(text, pages=(0, 1, 2, 3, 4, 5, 6, 7))

    extracted = sections.feature.toc.extract_toc_likelihood(text)
    extracted = [item.content.value for item in extracted]
    assert sum(extracted) == pytest.approx(1.0)
