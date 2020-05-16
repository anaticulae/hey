# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import textstyle.serialize


def test_doctextstyle_dump_load():
    result = textstyle.DocTextStyle()
    assert result

    dumped = textstyle.serialize.dump_docstyle(result)
    loaded = textstyle.serialize.load_docstyle(dumped)
    assert loaded == result
