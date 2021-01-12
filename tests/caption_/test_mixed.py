# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

import caption.path
import tests.caption_


def test_mixed_bachelor51_page30(testdir, monkeypatch):
    source = power.link(power.BACHELOR051_PDF)
    cmd = f'-i {source} --pages=30'
    tests.caption_.run(cmd, monkeypatch=monkeypatch)

    table = caption.path.table_caption(testdir.tmpdir)
    figure = caption.path.image_caption(testdir.tmpdir)

    table = serializeraw.load_captions(table)
    figure = serializeraw.load_captions(figure)

    figures = utila.select_content(figure, page=30)
    assert len(figures) == 1, str(figures)
    tables = utila.select_content(table, page=30)
    assert len(tables) == 1, str(tables)
