# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import words.headlines


class MultiLine(words.headlines.HeadlineExtractorStrategy):

    def should_skip(
            self,
            distance_tosmall,
            headline_tosmall,
            textfeed,
            lastitem,
    ):
        if distance_tosmall and headline_tosmall:
            return True
        if headline_tosmall:
            return True
        return False

    def smallest_headlinedistance(self):
        return 0

    def smallest_textsize(self):
        return 0
