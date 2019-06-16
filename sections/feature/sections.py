# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import Flag
from yaml import dump

from sections.ctor import Chapter
from sections.ctor import Index
from sections.ctor import TableOfContent
from sections.ctor import Text
from sections.ctor import TitlePage
from sections.ctor import WhitePage
from sections.feature import load_likelihood
from sections.feature.chapter import chapter_value_to_percent
from sections.feature.chapter import load_chapter_detection
from sections.feature.whitepage import load_whitepages
from sections.feature.whitepage import whitepage_value_to_percent


def work(
        chapter: str,
        index: str,
        title: str,
        toc: str,
        whitepage: str,
) -> str:
    chapter = load_chapter_detection(chapter)
    chapter = [chapter_value_to_percent(item) for item in chapter]

    index = load_likelihood(index)
    title = load_likelihood(title)
    toc = load_likelihood(toc)

    whitepage = load_whitepages(whitepage)
    whitepage = [whitepage_value_to_percent(item) for item in whitepage]

    builder = [Chapter, Index, TitlePage, TableOfContent, WhitePage]

    result = []
    for number, page in enumerate(zip(chapter, index, title, toc, whitepage)):
        # TODO:  What if more than one item is max? 1.0, 1.0?
        value = max(page)
        if value < 0.4:  # TODO: Holy value
            result.append(Text(start=number, end=number, trust=1.0))
            continue
        ctor = builder[page.index(value)]
        result.append(ctor(
            start=number,
            end=number,
            trust=value,
        ))

    dumped = dump_sections(result)
    return dumped


def dump_sections(pages):
    # convert to raw
    page = [item.__class__.__name__ for item in pages]

    result = dump(page)
    return result


def commandline():
    return Flag(
        longcut=name(),
        message='extract document structure from pdf file',
    )


def name():
    return 'sections'
