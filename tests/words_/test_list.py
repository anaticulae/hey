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
#pylint:disable=W0611
from tests.fixtures.restruct import RESTRUCT_HORIZONTAL
from tests.fixtures.restruct import RESTRUCT_PAGESIZE
from tests.fixtures.restruct import RESTRUCT_TEXT
from tests.fixtures.restruct import RESTRUCT_TEXT_POSITION
from tests.fixtures.restruct import restructured_headlines
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_positions
from tests.fixtures.restruct import restructured_textexample
from tests.fixtures.restruct import restructured_textexample_dumped
from tests.fixtures.simple import simple_contentborder
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_pagetextnavigators
from tests.fixtures.simple import simple_second_page_navigator
from tests.fixtures.simple import simple_second_page_size
from words.feature.list import LType
from words.feature.list import PageList
from words.feature.list import dump_lists
from words.feature.list import extract_lists
from words.feature.list import load_lists
from words.feature.list import parse_dotted_list
from words.feature.list import parse_numbered_list
from words.feature.list import work


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


def test_words_list_navigator_extract_lists(
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


def test_words_list_numbered_regex():

    parsed = parse_numbered_list(NUMBERED_LIST)

    assert len(parsed) == NUMBERED_LIST_SAMPLE_SIZE, parsed

    # Final example is very important!
    last_content, last_title = parsed[-1]
    assert last_title == '8.'
    assert last_content == (
        "Consider using optional static type checking to"
        " make sure your type usage works in both Python 2 &\n3 (e.g. use mypy "
        "to check your typing under both Python 2 & Python 3).")


def test_words_list_numbered_regex_single_item():
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


def test_words_list_dotted():
    parsed = parse_dotted_list(DOTTED_LIST)
    assert parsed == DOTTED_LIST_EXPECTED


DOTTED_EXAMPLE = """
For this project, we’ll have the following pages:
  • Index Page
    • Support
      • Installation
  • Cookbook/Examples
• Command Line Options
• Changelog
Let’s start with the Support page.
"""

DOTTED_EXAMPLE_EXPECTED = [
    'Index Page',
    'Support',
    'Installation',
    'Cookbook/Examples',
    'Command Line Options',
    'Changelog',
]


def test_words_list_dotted_with_start_and_end():
    parsed = parse_dotted_list(DOTTED_EXAMPLE)
    assert parsed == DOTTED_EXAMPLE_EXPECTED


DOTTED_EXAMPLE_CONTENT_ONLY = """ • Index Page
    • Support
• Changelog"""


def test_words_list_dotted_with_content_only():
    parsed = parse_dotted_list(DOTTED_EXAMPLE_CONTENT_ONLY)
    assert parsed == ['Index Page', 'Support', 'Changelog']


@fixture
def dumped_list(
        restructured_textexample_dumped,
        restructured_headlines,
):
    headlines = restructured_headlines
    undefined = restructured_textexample_dumped

    dumped = work(
        undefined,
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        headlines=headlines,
        border=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
    )
    return dumped


def test_words_list_work(dumped_list):
    assert len(dumped_list) > 400, str(dumped_list)

    result = load_lists(dumped_list)
    assert len(result) == 3, str(result)

    first_items = [item for (_, item) in result[0][1][0][2].data]
    second_items = [item for (_, item) in result[1][1][0][2].data]
    last_items = [item for (_, item) in result[2][1][0][2].data]

    assert len(first_items) == 15, str(first_items)
    assert first_items == [
        'Code: Block', 'Code: Inline', 'Emphasis: Italics', 'Emphasis: Strong',
        'Headers', 'Horizontal rules', 'Images: Inline', 'Line Return',
        'Links: Inline', 'Links: Inline with title', 'Links: Reference',
        'Lists: Simple', 'Lists: Nested', 'Paragraphs', 'Images: Reference'
    ]
    assert len(second_items) == 6, str(second_items)
    assert second_items == [
        'Index Page', 'Support', 'Installation', 'Cookbook/Examples',
        'Command Line Options', 'Changelog'
    ]
    assert len(last_items) == 3, str(last_items)
    assert last_items == ['genindex', 'modindex', 'search']


def test_words_list_dump_and_load_lists(dumped_list):
    loaded = load_lists(dumped_list)

    dumped = dump_lists(loaded)
    assert dumped == dumped_list
