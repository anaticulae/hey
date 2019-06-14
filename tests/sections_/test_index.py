# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from sections.feature.index import extract_index_likelihood
# pylint:disable=unused-import
from tests.sections_ import restructured_document

# manually set to secure index finder quality
LAST_PAGE_INDEX_LIKELYHOOD = 0.45


#pylint:disable=W0621
def test_extract_index_likelihood(restructured_document):
    result = extract_index_likelihood(restructured_document)
    assert 0.95 <= sum(result) <= 1.05

    # The index is on the last page
    last_page = result[-1]
    assert last_page >= LAST_PAGE_INDEX_LIKELYHOOD, result
