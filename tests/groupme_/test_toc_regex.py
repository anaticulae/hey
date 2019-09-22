# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import groupme.feature.toc
import groupme.toc.regex
import tests

MASTER_72PAGES_TEXT = tests.resources.text(
    tests.resources.MASTER_72PAGES,
    prefix='oneline',
)


def test_extract_toc_from_master_pages72_page_1and2():
    document = serializeraw.load_document(MASTER_72PAGES_TEXT)

    page1, page2 = document[1:3]

    result_page1 = groupme.toc.regex.parse_page(page1)
    assert len(result_page1) == 23
    assert all([not '...' in item.title for item in result_page1])

    result_page2 = groupme.toc.regex.parse_page(page2)
    assert len(result_page2) == 9
    assert all([not '...' in item.title for item in result_page2])


def test_extract_toc_from_master_pages72_page_withouttoc():
    document = serializeraw.load_document(MASTER_72PAGES_TEXT)

    result = groupme.toc.regex.parse_page(document[4:])

    assert not result, str(result)


FIRST_LINE = ('2.1 Web 2.0, Social Web und Social Media: '
              'Abgrenzungen und Definitionen   .............. 4')

SECOND_LINE = (
    '2.   Das Social Web und die Privatsphäre Selbstdarstellungsverhalten\n'
    'der Nutzer aus Sicht von Massenmedien und Literatur .... 4')

# TODO: INVESTIGATE IN FOLLOWING `    ` Whitespaces
# TODO: FIX REGEX_PATTERN


@pytest.mark.parametrize('content, expected', [
    (FIRST_LINE, [
        groupme.toc.TocLine(
            '2.1',
            'Web 2.0, Social Web und Social Media: Abgrenzungen und Definitionen',
            '4',
            FIRST_LINE,
        ),
    ]),
    (SECOND_LINE, [
        groupme.toc.TocLine(
            '2.',
            ('Das Social Web und die Privatsphäre Selbstdarstellungsverhalten\n'
             'der Nutzer aus Sicht von Massenmedien und Literatur'),
            '4',
            SECOND_LINE,
        )
    ])
])
def test_extract_toc_line(content, expected):
    parsed = groupme.toc.regex.parse(content)
    assert parsed == expected, str(parsed)
