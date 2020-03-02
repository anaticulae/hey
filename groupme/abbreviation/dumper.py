# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import yaml

import groupme.abbreviation
import groupme.abbreviation.parser


def dump_abbreviation_table(result: groupme.abbreviation.AbbreviationResult) -> str: # yapf:disable
    assert isinstance(result, groupme.abbreviation.AbbreviationResult), type(result) # yapf:disable
    raw = [groupme.abbreviation._dump_abbreviation(item) for item in result]  # pylint:disable=W0212
    dumped = yaml.dump(raw)
    return dumped


def load_abbreviation_table(content: str) -> groupme.abbreviation.AbbreviationResult: # yapf:disable
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)

    result = groupme.abbreviation.AbbreviationResult()
    for item in loaded:
        loaded = groupme.abbreviation._load_abbreviation(item)  # pylint:disable=W0212
        result.append(loaded)
    return result
