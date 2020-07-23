# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import texmex
import utila


def test_hey_navigator_merge_content():  # pylint:disable=W0621
    navigator = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.DOCU07_PDF))
    navigator = utila.select_page(navigator, page=1)
    content = texmex.navigator_to_content(navigator)
    merged, _ = texmex.merge_content(content)
    merged = texmex.merge_content_join(merged)

    content = texmex.navigator_to_content(navigator)
    merged, _ = texmex.merge_content(content)  # split content and merge_ids
    # NOTE: Dependens on `MAX_MERGE_DISTANCE`, not a good test?
    #     paragraph_after_merge = 8
    #     assert len(merged) == paragraph_after_merge
    merged_content = texmex.merge_content_join(merged)

    expectend_content = utila.NEWLINE.join([item.text for item in content])
    merged_content = utila.NEWLINE.join([item.text for item in merged_content])

    assert merged_content == expectend_content
    content_count = len(expectend_content)
    merged_count = len(merged_content)
    # ensure that no data is lost while merging
    assert content_count == merged_count


def test_hey_navigator_create_pagetextcontent_navigator_frompath():
    loaded = serializeraw.create_pagetextcontentnavigators_frompath(
        power.link(power.BACHELOR111_PDF),
        pages=(1, 2, 3, 4),
        prefix='oneline',
    )
    first = loaded[0]
    lasttext = first[-1].text
    assert lasttext != 'i', lasttext
