# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import itertools

import iamraw
import utila

import hey.fonts.store
import hey.textnavigator.navigator
import words.boxed
import words.feature
import words.headlines
import words.text
import words.text.paragraph
import words.text.sentence


def extract_texts(loaded: words.feature.TextRequiredResources):
    """Iterate thrue document via headline and process the content
    between the headlines. Split Chapter into paragraphs and paragraphs
    into sentences and words.

    Args:
        loaded: resources provided by text module
    Returns:
        list of text pages with textutal content definition
    """
    result = []
    # ensure to preserve correct page order when having pages without headline
    headlines = insert_empty_pages(loaded.headlines)
    # start analyzing
    for headline in headlines:
        analyzed = analyze_page(
            headline,
            loaded.fontstore,
            loaded.textnavigators,
            loaded.border,
            loaded.boxes,
        )
        if analyzed is None:
            # empty page
            continue
        result.append(analyzed)

    # sequeeze text
    # TODO: REQUIRE NEW INTERFACE
    result = [
        (page.page, words.text.sentence.find_sentences(page)) for page in result
    ]
    return result


def analyze_page(
        headlines,
        fontstore: hey.fonts.store.FontStore,
        textnavigators: hey.textnavigator.navigator.PageTextNavigator,
        border: iamraw.Border,
        boxes: words.boxed.BoxedChecker,
) -> words.text.PageTextWithHeadlines:
    assert headlines, 'empty `headlines`'
    # Seek pagetextnavigator to correct positon
    prepared = prepare_analyze_page(
        headlines,
        textnavigators,
        fontstore,
        border,
    )
    if prepared is None:
        # Skip analyzing empty pages
        return None

    call = functools.partial(
        words.text.paragraph.collect_paragraph,
        page=prepared.number,
        pcn=prepared.pagetextcontentnavigator,
        fcs=prepared.fontcontentstore,
        boxes=boxes,
    )
    zipped = itertools.zip_longest(
        prepared.headlines,
        prepared.headlines[1:],
        fillvalue=None,
    )

    # collect paragraphs
    result = [
        (first, call(first=first, second=second)) for (first, second) in zipped
    ]

    # clear result, remove empty content
    result = [(headline, content)
              for (headline, content) in result
              if (headline.container is not None and headline.container > -1)]

    return words.text.PageTextWithHeadlines(
        page=prepared.number,
        content=result,
    )


def prepare_analyze_page(
        headlines,
        textnavigators,
        fontstore,
        borders,
) -> words.text.PageAnalyzeResources:
    """Add dummy headline if required

    Some pages does not contain a headline or the headline starts after
    the first text content. Therefore adding a dummy headline is
    required to collect this content under the dummy headline.

    """
    page = headlines[0].page
    content = utila.select_page(borders, page=page)
    if content is None:
        return None

    pcn = hey.textnavigator.navigator.PageTextContentNavigator(
        textnavigator=utila.select_page(textnavigators, page=page),
        content=utila.select_page(borders, page=page),
    )
    if pcn.offset == (None, None):
        # empty page
        return None

    fontstore = hey.fonts.store.FontContentStore(fontstore, pcn, page)
    # pcn.offset[0] - 1: the "virtual" headline is one container element before
    # the first content.
    if headlines[0].container is None:
        # start with None-Container
        headlines[0].container = pcn.offset[0] - 1  # absolute coordinate
    elif headlines[0].container > pcn.offset[0]:
        # the page does not start with a headline, without inserting an empty
        # line the starting content of the page is ignored
        # -> add starting container
        headline = iamraw.Headline(
            text=None,
            level=None,
            rawlevel=None,
            page=page,
            container=pcn.offset[0] - 1,  # absoulte coordinate
        )
        headlines = [headline] + headlines
    else:
        # normal headline
        pass

    return words.text.PageAnalyzeResources(
        number=page,
        headlines=headlines,
        pagetextcontentnavigator=pcn,
        fontcontentstore=fontstore,
    )


def insert_empty_pages(headlines):
    """Add pages with content but without any headlines.

    What happens when we forget to fill the headlines? All pages without any
    headlines are ignored in content analyzis.
    """
    # fill headlines
    heads = []
    for first, second in itertools.zip_longest(
            utila.flatten(headlines),
            utila.flatten(headlines)[1:],
            fillvalue=None,
    ):
        heads.append(first)
        if second is None:
            utila.error('Implement fill last one till chapter ends')
            break
        for index in range(first.page + 1, second.page):
            heads.append(iamraw.Headline(text=None, level=None, page=index))

    headlines = [
        list(group) for _, group in itertools.groupby(heads, lambda x: x.page)
    ]
    return headlines
