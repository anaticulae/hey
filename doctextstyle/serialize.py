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

import doctextstyle


def load_docstyle(content: str) -> doctextstyle.DocTextStyle:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    return loaded


def dump_docstyle(style: doctextstyle.DocTextStyle) -> str:
    assert isinstance(style, doctextstyle.DocTextStyle)
    dumped = yaml.dump(style)
    return dumped
