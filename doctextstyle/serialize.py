# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import utila
import yaml

import doctextstyle.data


def load_docstyle(content: str) -> doctextstyle.data.DocTextStyle:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(content)
    result = doctextstyle.data.DocTextStyle(**loaded)
    return result


def dump_docstyle(style: doctextstyle.data.DocTextStyle) -> str:
    assert isinstance(style, doctextstyle.data.DocTextStyle)
    raw = dataclasses.asdict(style)
    dumped = yaml.safe_dump(raw)
    return dumped
