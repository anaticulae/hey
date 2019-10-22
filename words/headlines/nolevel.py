# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw
import utila

import hey.textnavigator.fonts
import words.headlines

SMALLEST_HEADLINE_DISTANCE = 1.2  # TODO: HOLY VALUE
SMALLEST_HEADLINE_TEXTSIZE = 1.1


class NoLevelHeadlineExtractor(words.headlines.HeadlineExtractorStrategy):

    def setup(self):
        super().setup()
        self.smallest_headlinedistance = utila.roundme(
            self.textdistance * SMALLEST_HEADLINE_DISTANCE)
        self.smallest_textsize = utila.roundme(
            self.textsize * SMALLEST_HEADLINE_TEXTSIZE)

    def extract_headline(
            self,
            text,
            textbounds,
            textdistances,
            page,
            containerid,
            content_area,
    ):
        contentstart, contentend = content_area
        distanceid = containerid - contentstart
        fontdistance = textdistances[distanceid]
        textsize = hey.textnavigator.fonts.fontsize_from_textbounds(textbounds)

        distance_tosmall = fontdistance < self.smallest_headlinedistance
        headline_tosmall = textsize < self.smallest_textsize
        last_item = distanceid == (contentend - 1)

        if distance_tosmall and headline_tosmall:
            return None
        if headline_tosmall:
            return None

        try:
            # TODO: IMPROVE LEVEL CALCULATION
            # Space after and before
            level = textdistances[distanceid]
            if last_item:
                # Headline is alone on the page end
                level = level * 2
            else:
                level = level + textdistances[distanceid + 1]
        except IndexError:
            level = textdistances[distanceid] * 2

        headline = iamraw.Headline(
            container=containerid,
            level=level,
            page=page,
            text=text,
        )
        return headline
