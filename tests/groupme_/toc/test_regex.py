# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import pytest
import serializeraw

import groupme.feature.toc
import groupme.toc.lineregex
import groupme.toc.strategy.regex as gtsr
import tests

MASTER72_TEXT = iamraw.path.text(tests.resources.MASTER72, prefix='oneline')


def test_extract_toc_from_master_pages72_page_1and2():
    document = serializeraw.load_document(MASTER72_TEXT)

    page1, page2 = document[1:3]

    result_page1 = gtsr.parse_page(page1)
    assert len(result_page1) == 23
    assert all([not '...' in item.title for item in result_page1])

    result_page2 = gtsr.parse_page(page2)
    assert len(result_page2) == 9
    assert all([not '...' in item.title for item in result_page2])


@pytest.mark.xfail(reason='regex is going crazy')
def test_extract_toc_from_master_pages72_page_withouttoc():
    document = serializeraw.load_document(MASTER72_TEXT)

    result = gtsr.parse_page(document[4:])

    assert not result, str(result)


FIRST_LINE = ('2.1 Web 2.0, Social Web und Social Media: '
              'Abgrenzungen und Definitionen   .............. 4')

SECOND_LINE = (
    '2.   Das Social Web und die Privatsphäre Selbstdarstellungsverhalten\n'
    'der Nutzer aus Sicht von Massenmedien und Literatur .... 4')

# TODO: INVESTIGATE IN FOLLOWING `    ` Whitespaces
# TODO: FIX REGEX_PATTERN


@pytest.mark.parametrize('content, expected', [
    pytest.param(
        FIRST_LINE,
        [
            groupme.toc.TocLine(
                '2.1',
                'Web 2.0, Social Web und Social Media: Abgrenzungen und Definitionen',
                '4',
                FIRST_LINE,
            ),
        ],
        id='first_line',
    ),
    pytest.param(
        SECOND_LINE,
        [
            groupme.toc.TocLine(
                '2.',
                ('Das Social Web und die Privatsphäre Selbstdarstellungsverhalten\n'
                 'der Nutzer aus Sicht von Massenmedien und Literatur'),
                '4',
                SECOND_LINE,
            )
        ],
        id='second_line',
    )
])
def test_extract_toc_line(content, expected):
    parsed = gtsr.parse(content)
    assert parsed == expected, str(parsed)


def test_extract_toc_line_whitespace_decision():
    """See design decission: We do not want to support following whitespaces."""

    text = '2. We do not want whitespaces at the end ......... 4     '
    parsed = gtsr.parse(text)
    assert not parsed, 'we do not want to support whitespaces'

    text = '       2. We do not want whitespaces at the end ......... 4'
    parsed = gtsr.parse(text)
    assert not parsed, 'we do not want to support whitespaces'

    text = '       2. We do not want whitespaces at the end ......... 4   '
    parsed = gtsr.parse(text)
    assert not parsed, 'we do not want to support whitespaces'


def test_groupme_toc_lineregex_parse():
    line = '2.2.3 Drahtlostechnologien fuer Nahbereichsnetzwerke (WPAN) 15'
    parsed = groupme.toc.lineregex.parse(line)
    assert parsed
