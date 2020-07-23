# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import power
import pytest
import utila
import utilatest

import tests

# this documents does not passes the current implementation
UNSUPPORTED_DOCUMENTS = {
    # 'paper/page_6_double_column.pdf',
}

EXPECTED_FAILURE = {  # yapf:disable
    # 'docu/twine.pdf': 'font extracting problem',
    'howto_argparse/howto_argparse.pdf': 'not every headlines can be detected',
    # ambigous sections, groupme works, words does not work
    # 'order/howtowrite_pages9.pdf': 'headline detection does not works correctly',
}

SKIP_DOCUMENTS = {
    'bachelor/page_111_images_toc.pdf',
    'bachelor/page_159_huge_appendix.pdf',
    'bachelor/page_37_tables.pdf',
    'bachelor/page_56_hard_to_read.pdf',
    'bachelor/page_63_images_toc.pdf',
    'docu/howto_argparse.pdf',
    'docu/twine.pdf',
    'docu/vimguide.pdf',
    'homework/page_40_images_toc.pdf',
    'homework/page_50_math.pdf',
    'master/page_116_images_toc_formular.pdf',
    'master/page_72_noimages_toc.pdf',
    'master/page_78_images_toc.pdf',
    'master/page_83_noimages_toc.pdf',
    'master/page_89_noimages_toc.pdf',
    'order/howtowrite_pages9.pdf',
    # requires to much required test time
    'order/page_38.pdf',
    'technical/page_24_color_figures_images.pdf',
}

HEADLINE_COUNT = {
    'howto_argparse/howto_argparse.pdf': 7,  # 9 with subsections
}


def params():
    # do not ignore any document, it's a nightly
    ignore = []
    pdf = [
        item for item in power.PDF if all([
            not tests.relative_path(item) in ignore,
            # skip generated pdfs to avoid double work
            not 'notitle' in item,
        ])
    ]
    result = []

    def determine_mark(pdf):
        relative = tests.relative_path(pdf)
        if relative in UNSUPPORTED_DOCUMENTS:
            return pytest.mark.xfail(reason='contains unsupported feature')
        with contextlib.suppress(KeyError):
            return pytest.mark.xfail(reason=EXPECTED_FAILURE[relative])
        return pytest.mark.huge

    for item in pdf:
        double = pytest.param(
            (
                item,
                '--char_margin 100.0 --boxes_flow 1.0',
                '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3',
            ),
            id=tests.relative_path(item),
            marks=determine_mark(item),
        )
        result.append(double)
    return result


@pytest.fixture(params=params())
def rawresult(request, testdir):
    tmpdir = testdir.tmpdir
    tocpath = os.path.join(tmpdir, 'toc')
    generalpath = os.path.join(tmpdir, 'general')
    for item in [tocpath, generalpath]:
        os.makedirs(item)

    pdf, toccmd, generalcmd = request.param
    rawtoc = f'rawmaker -i {pdf} -j=auto --pages=0:20 -o {tocpath} --prefix=oneline {toccmd}'
    rawgeneral = f'rawmaker -i {pdf} -j=auto --pages=0:20 -o {generalpath} {generalcmd}'
    linero = f'linero -o {generalpath}'

    done = utila.run(rawtoc)
    assert done.returncode == utila.SUCCESS, utila.format_completed(done)

    done = utila.run(rawgeneral)
    assert done.returncode == utila.SUCCESS, utila.format_completed(done)

    done = utila.run(linero)
    assert done.returncode == utila.SUCCESS, utila.format_completed(done)

    return (tmpdir, tocpath, generalpath)


@utilatest.skip_nightly
@pytest.mark.usefixtures('testdir')
def test_huge_running_application(rawresult):  # pylint:disable=W0621
    tmpdir, tocpath, generalpath = rawresult

    current = os.path.join(tmpdir, 'current')
    os.makedirs(current)

    runme = f'groupme -i {generalpath} -i {tocpath} -o {current} -j=auto'
    done = utila.run(runme)
    assert done.returncode == utila.SUCCESS, utila.format_completed(done)
