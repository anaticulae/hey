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
from functools import lru_cache
from functools import partial
from re import MULTILINE
from re import VERBOSE
from re import finditer
from typing import List
from typing import Tuple

from iamraw import Border
from utila import NEWLINE
from utila import Flag
from utila import checkdatatype
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from hey import CACHE_SMALL
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
        headlines: str,
        border: str,
        horizontals: str,
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
        horizontals,
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
        page, paragraphnumber, content = paragraph
        for mergednumber, (_, item) in enumerate(content):
            potentiallist = extract_lists(item, contentborder)
            if not potentiallist:
                # could not extract any list
                continue
            for listitem in potentiallist:
                result.append((paragraphnumber, mergednumber, listitem))
    if not result:
        return None
    return (page, result)


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
    area: List[int] = field(default_factory=list)

    def append(self, title: str, level: str = None):
        self.data.append((level, title))

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
    # TODO: MAX_Y_MERGE IS VERY INSTABLE
    unmerged = list(page)
    page, merged = merge_content(page, max_y_merge=15)  # TODO: HOLY VALUE
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
        #     print(ptextsize, textsize)
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
        pagelist = PageList()
        pagelist.area.extend(mergearea)
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
    result = [item.group(1).strip() for item in parsed]
    return result


def commandline() -> Flag:
    return Flag(
        longcut='list',
        message='Export list of extracted ordered and unordered lists',
    )


def dump_lists(lists: List[str]) -> str:
    raw = []
    for (number, page) in lists:
        pageresult = []
        for (paragraph, merged, content) in page:
            # Number, Item
            area = ' '.join([str(item) for item in content.area])
            content = ['%s %s' % (number, item) for (number, item) in content]
            pageresult.append({
                'area': area,
                'content': content,
                'id': '%d %d' % (paragraph, merged),
            })
        if pageresult:
            raw.append({
                'page': number,
                'lists': pageresult,
            })
    dumped = dump(raw)
    return dumped


@lru_cache(CACHE_SMALL)
def load_lists(content: str) -> List[str]:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        content = page['lists']
        newpage = []
        for listinstance in content:
            paragraph, merged = [
                int(item) for item in listinstance['id'].split()
            ]
            area = [int(item) for item in listinstance['area'].split()]
            instance = PageList(area=area)
            for entree in listinstance['content']:
                # See (Number, Item)
                number, text = entree.split(maxsplit=1)
                # # try to convert to int/float
                if number.isdigit():  # all decimal digits and not empty
                    number = int(number)
                instance.append(text, number)
            newpage.append((paragraph, merged, instance))
        result.append((pagenumber, newpage))
    return result
