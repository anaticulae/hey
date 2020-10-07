# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import serializeraw
import utilatest

import doctextstyle.cli
import tests.doctextstyle_
import tests.resources


def test_textstyle_cli_help(monkeypatch):
    tests.doctextstyle_.run('--help', monkeypatch=monkeypatch)


@utilatest.skip_longrun
def test_textstyle_cli(testdir, monkeypatch):
    source = power.link(power.MASTER072_PDF)
    outdir = os.path.join(testdir.tmpdir, 'helm/schelm')
    tests.doctextstyle_.run(f'-i {source} -o {outdir}', monkeypatch=monkeypatch)

    outpath = os.path.join(outdir, doctextstyle.cli.DEFAULT_OUTPUT_FILE)
    assert os.path.exists(outpath)

    docstyle = serializeraw.load_doctextstyle(outpath)
    assert docstyle
