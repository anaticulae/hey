# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import groupme.feature.footer
import tests.resources


@utila.skip_longrun
def test_groupme_footerheader_quality_bachelor111():
    dumped = groupme.feature.footer.work(
        tests.resources.text(tests.resources.BACHELOR111),
        tests.resources.text_positions(tests.resources.BACHELOR111),
        tests.resources.font_header(tests.resources.BACHELOR111),
        tests.resources.font_content(tests.resources.BACHELOR111),
        tests.resources.horizontals(tests.resources.BACHELOR111),
        tests.resources.sizeandborder(tests.resources.BACHELOR111),
        tests.resources.pagenumbers(tests.resources.BACHELOR111),
    )
    result = serializeraw.load_headerfooter(dumped)

    pages = list(range(1, 5))
    selected = [utila.select_page(result, page) for page in pages]

    extracted_pages = [item.page for item in selected]

    assert len(selected) == len(pages)
    assert extracted_pages == pages
