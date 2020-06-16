# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import magic.data


def test_dump_and_load_magic():
    data = [
        magic.data.PageContentContentType(
            page=5,
            content=[
                (1, magic.data.ContentType.UNDEFINED),
                (2, magic.data.ContentType.TEXT),
            ],
        ),
        magic.data.PageContentContentType(
            page=6,
            content=[
                (5, magic.data.ContentType.LIST),
                (6, magic.data.ContentType.TEXT),
            ],
        )
    ]
    dumped = magic.data.dump_types(data)
    loaded = magic.data.load_types(dumped)
    assert loaded == data
