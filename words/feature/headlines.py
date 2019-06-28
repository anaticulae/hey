# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example driven programming:

for chapter in document:
    for headline in chapter:
        print(headline)

Required resources:
    sections
    text
    font?
"""
from dataclasses import dataclass
from dataclasses import field
from statistics import mode
from typing import Tuple

from iamraw import Border
from iamraw import PageSize

from groupme.feature.footer import document_footer
from groupme.feature.footer import footerborder_to_bounds
from hey.fonts.store import FontStore
from hey.textnavigator.fonts import document_textsize
from hey.textnavigator.fonts import fontdistance
from hey.textnavigator.fonts import fontsize_from_textbounds
from hey.textnavigator.fonts import textbounds
from hey.textnavigator.fonts import textfeed
from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigator
from hey.textnavigator.navigator import navigator_to_bounds
from hey.textnavigator.navigator import percent_from_pagesize
from sections.feature.sections import Sections
from sections.feature.sections import chapters


@dataclass
class Headline:
    text: str
    level: int = field(default=0, compare=False)
    rawlevel: str = field(default=None, compare=False)


def work():
    pass


def document_border(contentborders) -> Border:
    # 'left bottom right top'
    left, bottom, right, top = [], [], [], []

    for item in contentborders:
        left.append(item[0])
        bottom.append(item[1])
        right.append(item[2])
        top.append(item[3])

    left, bottom, right, top = mode(left), mode(bottom), mode(right), mode(top)

    return Border(left, bottom, right, top)


def content_border(horizontals, contentborders):
    border = document_footer(horizontals)
    border = footerborder_to_bounds(border)
    leftright = document_border(contentborders)
    return Border(leftright.left, border.bottom, leftright.right, border.top)


def extract_headlines(
        sections: Sections,
        pagetextnavigator: PageTextNavigators,
        fontstore: FontStore,
        sizeandborder,
        horizontals,
        chapter: int = 0,
):
    chapter = [chapter] if isinstance(chapter, int) else chapter
    content = chapters(sections)
    pagesizes, contentborders = sizeandborder
    border = content_border(horizontals, contentborders)

    textsize = document_textsize(
        navigators=pagetextnavigator,
        contentborders=contentborders,
    ) * 1.1
    result = []
    font = fontstore.font(0, 0, line=0, char=0)
    for index in chapter:
        chaptercontent = []
        (start, end) = content[index]

        for number in range(start, end + 1):
            # TODO: FIX PageTextContentNavigator
            # pagesize = pagesizes[number]
            # contentborder = contentborders[number]
            # top, bottom = topbottom(pagesize, tb)
            pagecontent = PageTextContentNavigator(
                pagetextnavigator[number],
                border,
            )
            xoff = pagecontent.offset[0]
            xoff = xoff if xoff is not None else 0

            bounds = navigator_to_bounds(pagecontent)
            distances = fontdistance(bounds)
            bounds = textbounds(pagecontent, border)
            for containerid, (item, text) in enumerate(bounds, start=xoff):
                splitted = text.splitlines()
                if len(splitted) > 1:
                    continue
                fontsize = fontsize_from_textbounds(item)
                if fontsize <= textsize:
                    continue

                print('page: %d' % number)
                font = fontstore.font(number, containerid, line=1, char=1)
                print('Font %r' % font)
                print(fontsize)
                print(text)
                chaptercontent.append(Headline(
                    text=text,
                    level=fontsize,
                ))
                # for item in pagecontent:
                #     # fontsize =
                #     splitted = item[1].splitlines()
                #     if len(splitted) > 1:
                #         continue

                #                     def textbounds(
                #         navigator: 'PageTextNavigator',
                #         contentborder: Border,
                # ) -> TextBoundsList:
                # bounds, text = splitted[0]
                # textfeed()

                # print(splitted)
                # print(item[1])
                # print(type(item[1]))
            print()
            print('NewPage')
        result.append(chaptercontent)
    return result
