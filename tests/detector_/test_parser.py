# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from detector.parser import textblock_token

TOKEN = """Hello
My Name is Token


DoubleSpace

Single Space"""


def test_parser_textblock_token():
    splitted = textblock_token(TOKEN)
    assert len(splitted) == 3, str(splitted)

    first = 'Hello\nMy Name is Token'
    second = 'DoubleSpace'
    third = 'Single Space'

    assert splitted[0] == first, str(splitted[0])
    assert splitted[1] == second, str(splitted[1])
    assert splitted[2] == third, str(splitted[2])
