# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.toc.strategy
import hey.textnavigator.navigator as htn
import tests.resources


def headlines_frompath(path: str, pages=None):
    loaded = htn.create_pagetextcontentnavigators_frompath(
        path,
        pages=pages,
        prefix='oneline',
    )
    # result = [gtsg.analyse_page(item) for item in loaded]
    result = groupme.toc.strategy.load(content=loaded)
    return result


def master72_toc():
    return headlines_frompath(tests.resources.MASTER_72PAGES, pages=(1, 2))


def bachelor111_toc():
    return headlines_frompath(
        tests.resources.BACHELOR_111PAGES,
        pages=(1, 2, 3, 4),
    )


def technical24_toc():
    return headlines_frompath(tests.resources.TECHNICAL_24PAGES, pages=(1))
