# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import caption.path
import tests.caption_


def extract_captions(
        source,
        pages: str,
        testdir,
        monkeypatch,
        resultpath=None,
        selected='',
):
    resultpath = resultpath if resultpath else caption.path.image_caption
    source = power.link(source)
    cmd = f'-i {source} --pages={pages} {selected}'
    tests.caption_.run(cmd, monkeypatch=monkeypatch)

    path = resultpath(testdir.tmpdir)
    loaded = serializeraw.load_captions(path)
    return loaded
