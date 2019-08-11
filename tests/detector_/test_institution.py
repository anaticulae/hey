# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from functools import partial

from pytest import mark
from pytest import param

from detector.parser.institution import parse
from tests import prepare as prepare_name
from tests.fixtures.titlepage import FIRST
from tests.fixtures.titlepage import FIRST_INSTITUTION
from tests.fixtures.titlepage import SECOND
from tests.fixtures.titlepage import SECOND_INSTITUTION


def prepare(item):
    return prepare_name('institution_' + item)


@mark.parametrize('example, expected', [
    param(FIRST, FIRST_INSTITUTION, id=prepare(FIRST)),
    param(SECOND, SECOND_INSTITUTION, id=prepare(SECOND)),
])
def test_parser_institution_parse(example, expected):
    parsed, _ = parse(example)
    assert parsed == expected, str(parsed)
