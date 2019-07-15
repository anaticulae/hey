# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
<document>
<h1>Chapter 1</h1>
<p>
Hallo <b>bold</b>,

wie geht es ihnen?

<i>Danke</i> sehr <u>gut</u>
</p>
<h1>Chapter 2</h1>

<h1>Chapter 3</h1>
</document>

"""

from contextlib import suppress
from re import compile as re_compile

from serializeraw import load_headlines
from utila import checkdatatype
from utila import flatten

from hey.undefined import intindex
from words.feature.boxed import load_boxedcontent
from words.feature.list import load_lists
from words.feature.text import dump_text
from words.feature.text import load_text

PATTERN = re_compile(r'^[0-9]+u$')


class ListLookUp:
    # TODO: UNITE WITH BOXEDCHECKER!
    def __init__(self, lists):
        self.data = {}
        self.load(lists)

    def load(self, lists):
        index = 0
        for page, content in lists:
            for item in content:
                try:
                    self.data[page].append((item, index))
                except KeyError:
                    self.data[page] = [(item, index)]
                index += 1

    def search(self, page, headline, undefined):
        with suppress(KeyError):
            current = self.data[page]
            for ((_, _, content), index) in current:
                if undefined in content.area:
                    return index
        return None


class BoxLookUp:

    def __init__(self, boxes):
        self.data = {}
        self.load(boxes)

    def load(self, boxes):
        for line in boxes:
            page, content = line
            for item in content:
                boxid, _, items = item
                chained = flatten(items)  # support verschachtelte boxes
                for real in chained:
                    bounding, (bindex, bcontent) = real
                    uindexs = [uindex for (_, uindex, _) in bcontent]
                    self.append(page, bindex, uindexs)

    def append(self, page, boxid, uindex):
        if page not in self.data:
            self.data[page] = {}
        for item in uindex:
            self.data[page][item] = boxid

    def search(self, page, uindex):
        with suppress(KeyError):
            return self.data[page][uindex]
        return None


@checkdatatype
def work(
        text: str,
        headlines: str,
        lists: str,
        boxed: str,
) -> str:

    text, listlookup, boxlookup = prepare_input(headlines, text, boxed, lists)

    text = process_words(text, listlookup, boxlookup)

    dumped = dump_text(text)
    return dumped


def process_words(text, listlookup, boxlookup):
    # TODO: Copy before replacing, to avoid side effects
    for (page, pagecontent) in text:
        # headline,
        for (headline, headlinecontent) in pagecontent:
            for index, line in enumerate(headlinecontent):
                if not PATTERN.match(line):
                    continue
                undefined = intindex(line)
                searched = listlookup.search(
                    page,
                    headline.container,
                    undefined,
                )
                if searched is not None:
                    headlinecontent[index] = '%dl' % searched
                    continue
                searched = boxlookup.search(page, undefined)
                if searched is not None:
                    headlinecontent[index] = '%db' % searched
                    continue
    return text


def prepare_input(
        headlines: str,
        text: str,
        boxed: str,
        lists: str,
):
    headlines = load_headlines(headlines)
    text = load_text(text, headlines=headlines)
    boxed = load_boxedcontent(boxed)
    lists = load_lists(lists)
    listlookup = ListLookUp(lists)
    boxlookup = BoxLookUp(boxed)
    return text, listlookup, boxlookup
