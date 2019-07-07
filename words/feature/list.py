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

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from re import MULTILINE
from re import VERBOSE
from re import finditer
from typing import List
from typing import Tuple

from iamraw import Border
from utila import NEWLINE
from utila import Flag

from hey.textnavigator.fonts import TextBoundsList
from hey.textnavigator.fonts import textbounds
from hey.textnavigator.fonts import textfeed
from hey.textnavigator.navigator import merge_content


def work(text: str, textposition: str, pageborder: str) -> str:
    return ''


class LType(Enum):
    UNDEFINED = None
    AMBIGUOUS = '*1.+-'
    DOTTED = '*'
    NUMBERED = '123'
    NUMBERED_WITH_DOT = '1.5.9.'  # default style
    PLUSED = '+'
    MINUSED = '-'


@dataclass
class PageList:

    data: List[Tuple[str, str]] = field(default_factory=list)

    def append(self, title: str, level: str = None):
        self.data.append((title, level))

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def ltype(self):
        return LType.UNDEFINED


def extract_lists(
        page: TextBoundsList,
        pagesize: Border,
        # textnavigator  #PageTextContentNavigator,
) -> List[PageList]:
    """Extract lists out of document page. There are different types of Lists.

    Numbered... 1.2.3, I. II. III., + + +, - - -, * * *.

    Args:
        page:
        pagesize(Border): size of current page [left bottom right top]
    """
    page = merge_content(page)
    text_bounds = textbounds(
        page,
        pagesize,
    )
    # textsize = textsize_from_textbounds(page, pagesize)

    result = []
    for parapraph in text_bounds:
        bounds, text = parapraph
        # ptextsize = fontsize_from_textbounds(bounds)
        # if ptextsize != textsize:
        #     # TODO: Hier gibt es noch ein Problem mit der Berechnung der
        #     # Schriftgroesse, da der Zeilenabstand nicht beruecksichtigt wird
        #     print(ptextsize, textsize)
        #     # Collect lists only in text, avoid collecting in headlines
        #     continue
        feed = textfeed(bounds)
        if feed <= 0.0:
            # TODO: Improve this
            # no text feed
            continue

        numbered_list = []
        for parser in [
                parse_dotted_list,
                parse_minus_list,
                parse_numbered_list,
                parse_plus_list,
        ]:
            numbered_list = parser(text)
            # TODO: parse all and compare
            if numbered_list:
                break
        pagelist = PageList()
        for item in numbered_list:
            # remove newline
            if isinstance(item, str):
                pagelist.append(item, 0)
            else:
                content, level = item
                pagelist.append((content, level))
        result.append(pagelist)
    return result


def parse_dotted_list(content: str) -> List[str]:
    return parse_general_list(content, '•')


def parse_plus_list(content: str) -> List[str]:
    return parse_general_list(content, r'\+')


def parse_minus_list(content: str) -> List[str]:
    return parse_general_list(content, '-')


def parse_numbered_list(content: str):
    content = str(content)
    assert content
    # TODO: Single line does not parse without NEWLINE
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


NUMBERED_LIST_PATTERN = r"""
    ^(?P<LEVEL>[0-9]+\.[0-9]{0})           # list level e.g. 1. 4. 5.
    \s                                     # whitespace
    (?P<TEXT>(?:.+\s){1,7}?)               # list item content
    (?=[0-9]+\.\s?|$)                      # new list start or final newline
    """


def general_list_pattern(descriptor: str):
    general = r"""
        ^(?:%s\s)
        (?P<TEXT>(?:.+\s){1,7}?) # list item content
                                 # Final
        (?=%s\s?|                # next item
         $                       # final line
         |\w)                    # following text after last dot
    """
    return general % (descriptor, descriptor)


def parse_general_list(content: str, selector: str) -> List[str]:
    assert isinstance(content, str), str(content)
    pattern = general_list_pattern(selector)
    parsed = finditer(
        pattern,
        content,
        flags=MULTILINE | VERBOSE,
    )
    result = [item.group(1).strip() for item in parsed]
    return result


def commandline() -> Flag:
    return Flag(
        longcut='list',
        message='Export list of extracted ordered and unordered lists',
    )
