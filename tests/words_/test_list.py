# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture

from hey.textnavigator.navigator import TextBoundsList
from hey.textnavigator.navigator import merge_content
from hey.textnavigator.navigator import to_content
# from hey.textnavigator.navigator import PageTextContentNavigator
#pylint:disable=W0611
from tests.fixtures.simple import simple_contentborder
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_pagetextnavigators
from tests.fixtures.simple import simple_second_page_navigator
from tests.fixtures.simple import simple_second_page_size
from words.feature.list import LType
from words.feature.list import PageList
from words.feature.list import extract_lists
from words.feature.list import parse_dotted_list
from words.feature.list import parse_numbered_list


#pylint:disable=W0621
def test_list_extract_page(
        simple_document,
        simple_pagetextnavigators,
        simple_contentborder,
):
    page_1 = simple_document[1]
    navigator_1 = simple_pagetextnavigators[1]
    contentborder_1 = simple_contentborder[1]

    return
    navigator = PageTextContentNavigator(navigator_1, contentborder_1)
    # def create_pagetextnavigator(
    #         position,
    #         document: Document,
    # ) -> List[PageTextNavigator]:
    navigator.fontdistance()
    extracted = extract_page(page_1, navigator)
    assert len(extracted) == 1

    pagelist: PageList = extracted[0]

    assert len(pagelist) == 8
    assert pagelist.ltype() == LType.NUMBERED

    for index, (_, level) in enumerate(pagelist, start=1):
        assert level == '%d.' % index, index


@fixture
def simple_second_page_merged_content(simple_second_page_navigator,
                                     ) -> TextBoundsList:
    content = to_content(simple_second_page_navigator)
    merged = merge_content(content)
    return merged


def test_groupme_navigator_extract_lists(
        simple_second_page_merged_content,
        simple_second_page_size,
):
    expected = PageList()
    raw = [
        "Only worry about supporting Python 2.7",
        ("Make sure you have good test coverage (coverage.py can help; pip"
         " install coverage)"),
        "Learn the differences between Python 2 & 3",
        ("Use Futurize (or Modernize) to update your code (e.g. pip install"
         " future)"),
        ("Use Pylint to help make sure you don’t regress on your Python 3"
         " support (pip install pylint)"),
        ("Use caniusepython3 to find out which of your dependencies are"
         " blocking your use of Python 3 (pip\n"
         "install caniusepython3)"),
        ("Once your dependencies are no longer blocking you, use continuous"
         " integration to make sure you stay\n"
         "compatible with Python 2 & 3"
         " (tox can help test against multiple versions of Python; pip install\n"
         "tox)"),
        ("Consider using optional static type checking to make sure your type"
         " usage works in both Python 2 &\n"
         "3 (e.g. use mypy to check your typing under both Python 2 & Python 3)."
        ),
    ]

    for index, item in enumerate(raw, start=1):
        expected.append(item, '%d.' % index)
    expected = [expected]
    extracted = extract_lists(
        simple_second_page_merged_content,
        simple_second_page_size,
    )
    assert extracted == expected


NUMBERED_LIST_SAMPLE_SIZE = 9
NUMBERED_LIST = """
6. Use caniusepython3 to find out which of your dependencies are blocking your use of Python 3 (pip
install caniusepython3)

To make your project be single-source Python 2/3 compatible, the basic steps are:

1. Only worry about supporting Python 2.7
2. Make sure you have good test coverage (coverage.py can help; pip install coverage)
3. Learn the differences between Python 2 & 3
4. Use Futurize (or Modernize) to update your code (e.g. pip install future)
5. Use Pylint to help make sure you don’t regress on your Python 3 support (pip install pylint)
6. Use caniusepython3 to find out which of your dependencies are blocking your use of Python 3 (pip
install caniusepython3)

7. Once your dependencies are no longer blocking you, use continuous integration to make sure you stay
compatible with Python 2 & 3 (tox can help test against multiple versions of Python; pip install
tox)

8. Consider using optional static type checking to make sure your type usage works in both Python 2 &
3 (e.g. use mypy to check your typing under both Python 2 & Python 3).

Text
"""


def test_groupme_words_list_numbered_regex():

    parsed = parse_numbered_list(NUMBERED_LIST)

    assert len(parsed) == NUMBERED_LIST_SAMPLE_SIZE, parsed

    # Final example is very important!
    last_content, last_title = parsed[-1]
    assert last_title == '8.'
    assert last_content == (
        "Consider using optional static type checking to"
        " make sure your type usage works in both Python 2 &\n3 (e.g. use mypy "
        "to check your typing under both Python 2 & Python 3).")


def test_groupme_words_list_numbered_regex_single_item():
    raw = (
        "8. Consider using optional static type checking to make sure your "
        "type usage works in both Python 2 &\n3 (e.g. use mypy to check your "
        "typing under both Python 2 & Python 3).")

    parsed = parse_numbered_list(raw)
    assert len(parsed) == 1
    level = parsed[0][1]
    assert level == "8."


DOTTED_LIST = """
Basics
Improving upon the pattern established at:
• Code: Block
• Code: Inline
• Emphasis: Italics
• Emphasis: Strong
• Headers
• Horizontal rules
  more than one line
  futher more lines
• Images: Inline
• Line Return
• Links: Inline
• Links: Inline with title
• Links: Reference
• Lists: Simple
• Lists: Nested
• Paragraphs
• Images: Reference
Futher text
"""

DOTTED_LIST_EXPECTED = [
    'Code: Block',
    'Code: Inline',
    'Emphasis: Italics',
    'Emphasis: Strong',
    'Headers',
    'Horizontal rules\n  more than one line\n  futher more lines',
    'Images: Inline',
    'Line Return',
    'Links: Inline',
    'Links: Inline with title',
    'Links: Reference',
    'Lists: Simple',
    'Lists: Nested',
    'Paragraphs',
    'Images: Reference',
]


def test_groupme_words_list_dotted():
    parsed = parse_dotted_list(DOTTED_LIST)

    assert parsed == DOTTED_LIST_EXPECTED
