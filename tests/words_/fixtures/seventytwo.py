# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests.resources
import words.feature


def textrequired(pages=None):
    return words.feature.load_resources_frompath(
        tests.resources.MASTER_72PAGES,
        pages=pages,
    )
