# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from iamraw import Font
from pytest import approx
from pytest import mark
from serializeraw import dump_likelihood
from serializeraw import load_likelihood

from sections.feature.title import extract_title_likelihood
from sections.textprocessor import split_page
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_fontstore_fixture
from tests.fixtures.restruct import restructured_text
from tests.fixtures.restruct import restructured_text_fixture
from tests.fixtures.simple import simple_document  # pylint:disable=W0611
from tests.fixtures.simple import simple_document_fixture
from tests.fixtures.simple import simple_fontstore  # pylint:disable=W0611
from tests.fixtures.simple import simple_fontstore_fixture


def test_load_font_lookup(restructured_fontstore):  #pylint:disable=W0621
    first_font = restructured_fontstore.font(
        number=0,
        container=0,
        line=2,
        char=0,
    )

    assert first_font
    assert isinstance(first_font, Font)


# qualitygate for further alogrithm improvements
MIN_TITLE_LIKELIHOOD = 0.70


# TODO: google: pytest + parametrize + fixture
@mark.parametrize('document,fontstore', [
    (restructured_text_fixture(), restructured_fontstore_fixture()),
    (simple_document_fixture(), simple_fontstore_fixture()),
])
def test_extract_title_likelihood(
        document,
        fontstore,
):
    result = extract_title_likelihood(
        document,
        fontstore,
    )
    assert result[0].content.value >= MIN_TITLE_LIKELIHOOD
    # as a result of rounding the sum of the likelihoods is not one, but thats
    # not a big problem, hitting the region one is enough.
    result = [item.content.value for item in result]
    assert sum(result) == approx(1.0, abs=0.05)


# TODO: Move to more general package
# TODO Investigate on this example. Page number must have a different font
@mark.parametrize(
    'page,position,expected',
    [
        (
            0,
            [
                (0, 2, 0),
                (2, 0, 0),
                (3, 0, 0),
                (4, 0, 0),
                # (3, 0, 12),
                # (3, 0, 12),
            ],
            [
                'The RestructuredText Book\nDocumentation',
                'Release 0.1',
                'Daniel Greenfeld, Eric Holscher',
                'Sep 27, 2017',
            ],
        ),
        (
            1,
            [],
            [],
        ),
        (
            2,
            [
                (1, 0, 0),
                (3, 1, 0),
                (5, 0, 0),
                (7, 1, 0),
                (9, 0, 0),
                (17, 0, 0),
            ],
            [
                'Contents',
                ('1 RestructuredText Tutorial\n'
                 '3\n'
                 '2 RestructuredText Guide'),
                ('5\n'
                 '2.1 Basics . . . . . . . . . . . . . . . . . . . . . . . . . . '
                 '. . . . . . . . . . . . . . . . . . . . . . . . . 5\n'
                 '2.2 Blockquotes . . . . . . . . . . . . . . . . . . . . . . . '
                 '. . . . . . . . . . . . . . . . . . . . . . . . 6\n'
                 '2.3 Code: Block . . . . . . . . . . . . . . . . . . . . . . . '
                 '. . . . . . . . . . . . . . . . . . . . . . . . 6'),
                ('3 RestructuredText Customizations\n'
                 '7\n'
                 '4 Sphinx Tutorial'),
                '9\n'
                '4.1 Step 1 . . . . . . . . . . . . . . . . . . . . . . . . . . '
                '. . . . . . . . . . . . . . . . . . . . . . . . . 9\n'
                '4.2 Step 2 . . . . . . . . . . . . . . . . . . . . . . . . . . '
                '. . . . . . . . . . . . . . . . . . . . . . . . . 13',
                ('5 Sphinx Guide\n'
                 '6 Sphinx Customizations\n'
                 '7 Testing your Documentation\n'
                 '8 Indices and tables\n'
                 '15\n'
                 '17\n'
                 '19\n'
                 '21'),
                ('i'),
            ],
        )
    ])
def test_split_page(
        restructured_text,  #pylint:disable=W0621
        page,
        position,
        expected,
):
    first_page = restructured_text[page]

    result = split_page(first_page, position)
    assert result == expected


def test_dump_and_load_likelhood(
        restructured_text,  #pylint:disable=W0621
        restructured_fontstore,  #pylint:disable=W0621
):
    result = extract_title_likelihood(
        restructured_text,
        restructured_fontstore,
    )
    dumped = dump_likelihood(result)
    loaded = load_likelihood(dumped)

    assert loaded == result
