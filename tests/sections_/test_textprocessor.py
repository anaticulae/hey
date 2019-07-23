# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from serializeraw import load_document
from serializeraw import load_font_content
from serializeraw import load_font_header

from hey.fonts.store import FontStore
from sections.feature.title import font_positions_from_page
from sections.textprocessor import PageIter
from tests.resources import PYPORTING_FONT_CONTENT
from tests.resources import PYPORTING_FONT_HEADER
from tests.resources import PYPORTING_TEXT


def pyporting_pages(pagenumber):  #pagenumber: int):
    document = load_document(PYPORTING_TEXT)
    current_page = document[pagenumber]

    header = load_font_header(PYPORTING_FONT_HEADER)
    content = load_font_content(PYPORTING_FONT_CONTENT)
    fontstore = FontStore(header, content)

    positions = font_positions_from_page(fontstore, pagenumber)

    pageiter = PageIter(page=current_page)
    return pageiter, positions


def test_sections_textprocessor_small_snippet_page2():
    pageiter, _ = pyporting_pages(2)
    first = pageiter.next(1, 0, 0)
    second = pageiter.next(1, 0, 7)
    third = pageiter.next(2, 0, 0)
    fourth = pageiter.next(2, 2, 6)
    fifth = pageiter.next(4, 0, 0)
    # TODO: Investigate newline at the end of line
    assert first == '(continued from previous page)\n'
    assert second == 'return '
    assert third == 'NULL;\n'

    assert fourth == ('result = PyBytes_FromString(encoded);\n'
                      'free(encoded);\n'
                      'return'), fourth

    assert fifth == (' result;\n' '}\n')


def test_sections_textprocessor_small_snippet_page7():
    pageiter, _ = pyporting_pages(6)

    selections = [
        ((1, 0, 0), '(continued from previous page)\n'),
        ((1, 0, 5), 'char '),
        ((1, 1, 0), '*trace;\n'),
        ((1, 1, 7), 'size_t '),
        ((1, 1, 42), 'name_length = (strlen(name) + 1) * '),
        ((1, 1, 48), 'sizeof'),
        ((1, 1, 49), '('),
        ((1, 1, 53), 'char'),
        ((1, 2, 0), ');\n'),
    ]
    for item, text in selections:
        collected = pageiter.next(*item)
        assert collected == text, collected


def test_sections_textprocessor_example_pyporting_page_2():
    pageiter, positions = pyporting_pages(2)

    result = []
    for item in positions:
        extracted = pageiter.next(*item).strip()
        result.append(extracted)
