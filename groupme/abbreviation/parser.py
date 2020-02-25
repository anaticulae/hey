# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.abbreviation
import groupme.abbreviation.simple
import hey.textnavigator.navigator


def parse(items: hey.textnavigator.navigator.PageTextNavigator,
         ) -> groupme.abbreviation.AbbreviationResult:
    assert isinstance(items, list), type(items)
    loaded = groupme.abbreviation.AbbreviationData(content=items)

    strategy = groupme.abbreviation.simple.SimpleAbbreviationParser(loaded)
    result = strategy.result()
    return result
