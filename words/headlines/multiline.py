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

import hey.textnavigator.fonts as htf
import hey.textnavigator.multiline as htm
import hey.textnavigator.navigator as htn
import words.headlines
import words.headlines.standard as whs


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

    def extract_page(
            self,
            pagecontent: htn.PageTextNavigator,
    ) -> words.headlines.Headlines:
        """Extract headlines on selected page

        Args:
            pagecontent: content of page to extract headlines
        Returns:
            Extracted list of iamraw.Headline.
        """
        result = []
        grouped = htm.group_page_by_fontsize(pagecontent)
        for items in grouped:
            text = ' '.join([item.text for item in items])
            parsed = whs.parse_headline(text)
            if not parsed:
                continue
            text = normalize_whitespaces(text)
            # TODO: REPLACE WITH LEVEL DETERMINER
            rawlevel = parsed['level'].strip()
            level = rawlevel.count('.') + 1
            if rawlevel.endswith('.'):
                level = 1
            if len(items) == 1:
                container = items.firstid
            else:
                container = (items.firstid, items.firstid + len(items) - 1)
            headline = iamraw.Headline(
                container=container,
                level=level,
                page=pagecontent.page,
                rawlevel=rawlevel,
                text=text,
            )
            result.append(headline)
        return result


def normalize_whitespaces(line):
    token = [item for item in line.split(' ') if item]
    return ' '.join(token)
