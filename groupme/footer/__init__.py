# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def strategies():
    import groupme.footer.strategy.common
    import groupme.footer.strategy.fixed
    import groupme.footer.strategy.moving
    import groupme.footer.strategy.pages
    import groupme.footer.strategy.plainmoving
    # TODO: Automate collection
    result = [
        groupme.footer.strategy.common.CommonTextStrategy,
        groupme.footer.strategy.fixed.FixedFooterStrategy,
        groupme.footer.strategy.moving.MovingFooterStrategy,
        groupme.footer.strategy.pages.PageNumberStrategy,
        groupme.footer.strategy.plainmoving.PlainMovingFooterStrategy
    ]
    return result
