# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.footer.headnotes


def test_parse_headnotes():
    """Test parsing headnotes based on contemporary"""
    raw = "INHALTSVERZEICHNIS"
    parsed = groupme.footer.headnotes.parse_title(raw)
    assert parsed.title == 'Inhaltsverzeichnis'
    assert parsed.raw == raw
