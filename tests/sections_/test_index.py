# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import serializeraw

import sections.feature.index
import tests.resources
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_text

# manually set to secure index finder quality, TODO: investigate later
LAST_PAGE_INDEX_LIKELYHOOD = 0.45


#pylint:disable=W0621
def test_extract_index_likelihood(restructured_text):
    result = sections.feature.index.extract_index_likelihood(restructured_text)
    result = [item.content.value for item in result]
    assert 0.95 <= sum(result) <= 1.05

    # The index is on the last page
    last_page = result[-1]
    assert last_page >= LAST_PAGE_INDEX_LIKELYHOOD, result


def test_index_work():
    dumped = sections.feature.index.work(tests.resources.RESTRUCT_ONELINE_TEXT)
    assert len(dumped) > 100


def test_hey_sections_feature_index_extract_index_likelihood():
    """Reduce false detection of index-pages"""
    path = tests.resources.text(tests.resources.HOWTO_ARGPARSE)
    document = serializeraw.load_document(path)

    result = sections.feature.index.extract_index_likelihood(document)

    # lower than five percent
    lower_than_five_percent = [item.content.value < 0.05 for item in result]
    assert all(lower_than_five_percent), lower_than_five_percent
