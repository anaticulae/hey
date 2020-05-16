# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import tests.resources
import tests.textstyle_
import textstyle.cli
import textstyle.serialize


def test_textstyle_cli_help(monkeypatch):
    tests.textstyle_.run('--help', monkeypatch=monkeypatch)


def test_textstyle_cli(testdir, monkeypatch):
    source = tests.resources.MASTER72
    outdir = os.path.join(testdir.tmpdir, 'helm/schelm')
    tests.textstyle_.run(f'-i {source} -o {outdir}', monkeypatch=monkeypatch)

    outpath = os.path.join(outdir, textstyle.cli.DEFAULT_OUTPUT_FILE)
    assert os.path.exists(outpath)

    docstyle = textstyle.serialize.load_docstyle(outpath)
    assert docstyle
