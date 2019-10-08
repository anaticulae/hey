# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""There are 2 different types of list:

    * the ordered (1.,2.,3.,...)
    * dotted, plus, minus - list (* Bratwurst, * Currwurst, +, -.)

     - load extracted text
     - filter undefined areas
     - check undefined area that area is list

"""
from functools import partial
from re import MULTILINE
from re import VERBOSE
from re import finditer
from typing import List

import utila
from iamraw import Border
from iamraw import PageList
from serializeraw import dump_lists
from utila import NEWLINE
from utila import Flag
from utila import checkdatatype

from hey.textnavigator.fonts import TextBoundsList
from hey.textnavigator.fonts import textbounds
from hey.textnavigator.fonts import textfeed
from hey.textnavigator.navigator import merge_content
from hey.textnavigator.navigator import merge_content_join
from words.input import prepare_input
from words.input import process_input


@checkdatatype
def work(
        extracted_text: str,
        text: str,
        text_position: str,
        border: str,
        headlines: str,
        headerfooters: str,
) -> str:
    """Combine `extracted_text` and check the `undefined` fields for lists

    Args:
        extracted_text(str): document with `undefined fields` from `text`
                             module of `words`
        text(str): extracted text from rawmaker
        text_position(str): position of extracted text
        headlines(str): extracted chapter/paragraph headlines of `words` module
        border(str):
    """
    extracted, contentborder = prepare_input(
        extracted_text,
        text,
        text_position,
        border,
        headlines,
        headerfooters,
    )

    result = process(extracted, contentborder)

    return dump_lists(result)


def process(extracted, contentborder):
    worker = partial(process_page, contentborder=contentborder)
    result = process_input(
        extracted,
        worker,
    )
    return result


def process_page(pagecontent, contentborder: Border):
    """
    Args:

    Returns:

    Format:
        page 5
            paragraphnumber, mergednumber, list
            0                1             []
            0                3             []
            0                4             []
            3                1             []
    """
    result, page = [], -1
    for paragraph in pagecontent:
        page, paragraphnumber, (content, uindexs) = paragraph
        zipped = enumerate(zip(content, uindexs))
        for mergednumber, ((_, item), uindex) in zipped:
            potentiallist = extract_lists(
                item,
                utila.select_page(contentborder, page=page),
                uindex,
            )
            if not potentiallist:
                # could not extract any list
                continue
            for listitem in potentiallist:
                result.append((paragraphnumber, mergednumber, listitem))
    if not result:
        return None
    return (page, result)


def extract_lists(
        page: TextBoundsList,
        pagesize: Border,
        uindex=None,
        # textnavigator  #PageTextContentNavigator,
) -> List[PageList]:
    """Extract lists out of document page. There are different types of Lists.

    Numbered... 1.2.3, I. II. III., + + +, - - -, * * *.

    Args:
        page:
        pagesize(Border): size of current page [left bottom right top]
    """
    # TODO: MAX_Y_MERGE IS VERY INSTABLE
    unmerged = list(page)
    page, merged = merge_content(
        page,
        # TODO: HOLY VALUE
        max_y_merge=15,
        uindex=uindex,
    )
    page_str = merge_content_join(page)
    text_bounds = textbounds(
        page_str,
        pagesize,
    )
    # textsize = textsize_from_textbounds(page, pagesize)
    result = []
    enumerated = enumerate(zip(text_bounds, merged))
    for paraindex, (paragraph, mergearea) in enumerated:
        bounds, text = paragraph
        # ptextsize = fontsize_from_textbounds(bounds)
        # if ptextsize != textsize:
        #     # TODO: Hier gibt es noch ein Problem mit der Berechnung der
        #     # Schriftgroesse, da der Zeilenabstand nicht beruecksichtigt wird
        #     # Collect lists only in text, avoid collecting in headlines
        #     continue
        feed = textfeed(bounds)
        # if feed <= 0.0:
        #     # TODO: Improve this
        #     # no text feed
        #     continue
        detected = []
        for parser in [
                parse_dotted_list,
                parse_minus_list,
                parse_numbered_list,
                parse_plus_list,
        ]:
            detected = parser(text)
            # TODO: parse all and compare
            if detected:
                break
        # parsing was not succesfull
        if not detected:
            continue
        pagelist = PageList(area=mergearea)
        # before, after = before_and_after(text, position[0], position[1])
        for index, item in enumerate(detected):
            # remove newline
            if isinstance(item, str):
                pagelist.append(item, index)
            else:
                content, level = item
                pagelist.append(content, level)

        if pagelist:
            result.append(pagelist)
    return result


def parse_dotted_list(content: str) -> List[str]:
    return parse_general_list(content, '•')


def parse_plus_list(content: str) -> List[str]:
    return parse_general_list(content, r'\+')


def parse_minus_list(content: str) -> List[str]:
    return parse_general_list(content, '-')


def parse_numbered_list(content: str):
    """Parse 1.2.3. list

    Args:
        content(str):
    Returns:
        list with (text, level) of list items
        None if nothing no list is parsed
    """
    content = str(content)
    assert content
    # TODO: WORKAROUND: Single line does not parse without NEWLINE
    if not content.endswith(NEWLINE):
        content += NEWLINE

    parsed = finditer(
        NUMBERED_LIST_PATTERN,
        content,
        flags=MULTILINE | VERBOSE,
    )
    if not parsed:
        return []
    result = []
    for item in parsed:
        start, _ = item.span()
        if start > 0:
            before = content[start - 1]
            if before != NEWLINE:
                # item is not located at the start of the text
                continue
        level, text = item[1], item[2]
        result.append((
            text.strip(),
            level,
        ))
    return result


# TODO: Merge both pattern!
NUMBERED_LIST_PATTERN = r"""
    ^(?P<LEVEL>[0-9]+\.[0-9]{0})           # list level e.g. 1. 4. 5.
    \s                                     # whitespace
    (?P<TEXT>(?:.+\s){1,7}?)               # list item content
    (?=[0-9]+\.\s?|$)                      # new list start or final newline
    """


def general_list_pattern(descriptor: str):
    # TODO: refactor pattern, this pattern looks not very beautiful
    general = r"""
        ^[ ]{0,20}(?:%s\s)       # possible Whitespaces at front and DESCRIPTOR
        (?P<TEXT>(?:.+\s){1,7}?) # list item content
                                 # Final
        (?=[ ]{0,20}%s\s?|       # next item possible Whitespace and DESCRIPTOR
         $                       # final line
         |\w)                    # following text after last dot
    """
    return general % (descriptor, descriptor)


def parse_general_list(content: str, selector: str) -> List[str]:
    assert isinstance(content, str), type(content)
    pattern = general_list_pattern(selector)

    # Workaround: Adding newline to content. The regex does not work, if the
    # content ends with a newline. TODO: Improve regex
    content = content + NEWLINE
    parsed = finditer(
        pattern,
        content,
        flags=MULTILINE | VERBOSE,
    )
    result = []
    for item in parsed:
        result.append(item.group(1).strip())
    return result


def commandline() -> Flag:
    return Flag(
        longcut='list',
        message='Export list of extracted ordered and unordered lists',
    )
