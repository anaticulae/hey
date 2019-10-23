# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re

import iamraw
import utila

import hey.fonts.store
import hey.textnavigator.fonts
import hey.textnavigator.navigator
import hey.utils
import words.headlines

MIN_DOTTED_COUNT = 0.1  # TODO: HOLY VALUE

SMALLEST_HEADLINE_DISTANCE = 1.05  # TODO:HOLY VALUE


class StandardHeadlineExtractor(words.headlines.HeadlineExtractorStrategy):

    def setup(self):
        super().setup()
        self.smallest_headlinedistance = SMALLEST_HEADLINE_DISTANCE * self.textdistance

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
        # fontsize = fontsize_from_textbounds(item)
        distanceid = containerid - contentstart  # TODO: -1
        fontdistance = textdistances[distanceid]

        # headline_tosmall = fontsize <= smallest_headlinesize
        distance_tosmall = fontdistance <= self.smallest_headlinedistance
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

    def filter(self, items):
        items = super().filter(items)
        items = filter_headlines(items)
        return items


def filter_headlines(items: iamraw.PagesHeadlineList):
    if isinstance(items, list):
        items = {index: value for index, value in enumerate(items)}

    result = collections.defaultdict(list)
    for chapter, content in items.items():
        chapter_headlines = []
        for headline in content:
            parsed = parse_headline(headline.text)
            if parsed:
                chapter_headlines.append(headline)
                continue
            if headline.text in words.headlines.WHITELIST:
                chapter_headlines.append(headline)
                continue
        result[chapter].extend(chapter_headlines)
    result = dict(result)  # require KeyError
    return result


def parse_headline(line):
    line = line.strip()
    return re.match(HEADLINE, line) is not None


# TODO: CODE DUPLICATION, COLLECT DIFFERENT HEADLINE PARSING APPROACHES AND
# CONVERT TO SINGLE ONE.
USER_CONTENT = r'\w\d\.&:, \-' + hey.utils.SPECIAL_MINUS_SIGN
# \W to ensure non-unicode character, like special - chars
HEADLINE = re.compile(
    (
        r'^'
        r'(?P<level>(\d{1,2}\.?)+\d{0,2})'
        r'[ ]{1,5}'
        r'(?P<text>\w'  # ensure that text does not start with whitespace
        fr'[{USER_CONTENT}]+?)'
        r'$'),
    re.VERBOSE,
)


def isdotted(items):
    assert items
    flat = utila.flatten(items)

    dotted = [item for item in flat if parse_headline(item.text)]
    percent = len(dotted) / len(flat)

    return percent >= MIN_DOTTED_COUNT
