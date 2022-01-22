# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import tests.caption_


def test_listing_bachelor111p45(testdir, monkeypatch):
    source = power.link(power.BACHELOR111_PDF)
    cmd = f'-i {source} --pages=45 --code'
    tests.caption_.run(cmd, monkeypatch=monkeypatch)
    codes = testdir.tmpdir.join('caption__code_caption.yaml')
    codes = serializeraw.load_captions(codes)
    assert len(codes) == 1
    expected = 'Listing 4.1: Auszug aus der Gruppen-Konfigurationsdatei der ETS'
    caption = codes[0].content[0].raw
    assert caption == expected
