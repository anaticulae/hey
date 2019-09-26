# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw

import words.headlines

SMALLEST_HEADLINE_SIZE = 1.1  # TODO: HOLY VALUE


class NoLevelHeadlineExtractor(words.headlines.HeadlineExtractorStrategy):

    def setup(self):
        super().setup()
        self.smallest_headlinedistance = self.textdistance * SMALLEST_HEADLINE_SIZE

    def extract_headline(
            self,
            text,
            textbounds,
            textdistances,
            page,
            containerid,
            contentstart,
    ):
        distanceid = containerid - contentstart + 1
        fontdistance = textdistances[distanceid]

        # headline_tosmall = fontsize <= smallest_headlinesize
        distance_tosmall = fontdistance < self.smallest_headlinedistance

        if distance_tosmall:
            return None
        try:
            # TODO: IMPROVE LEVEL CALCULATION
            # Space after and before
            level = textdistances[distanceid] + textdistances[distanceid + 1]
        except IndexError:
            level = textdistances[distanceid] * 2

        headline = iamraw.Headline(
            container=containerid,
            level=level,
            page=page,
            text=text,
        )
        return headline
