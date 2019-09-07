# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import join

from pytest import fixture
from pytest import mark
from pytest import param
from utila import SUCCESS
from utila import log
from utila import run
from utila import skip_longrun

from tests import pdfs
from tests import relative_path

# TODO: Reduce list of unsupported documents
# this documents does not passes the current implementation
UNSUPPORTED_DOCUMENTS = {
    'paper/page_6_double_column_with_math.pdf',
    'master/page_78_images_toc.pdf',
}

SKIP_DOCUMENTS = {
    'bachelor/page_111_images_toc.pdf',
    'bachelor/page_63_images_toc.pdf',
    'docu/vimguide.pdf',
    'homework/page_40_images_toc.pdf',
    'master/page_116_images_toc_formular.pdf',
    'master/page_72_noimages_toc.pdf',
    'master/page_78_images_toc.pdf',
    'master/page_83_noimages_toc.pdf',
    'master/page_89_noimages_toc.pdf',
}


def params():
    pdf = pdfs()
    # skip documents cause of to few computing power
    pdf = [item for item in pdf if not relative_path(item) in SKIP_DOCUMENTS]
    # select 5 items to reduce required test power
    # random is not good when reproducing an error, may use it later.
    pdf = pdf[0:5]
    result = []
    for item in pdf:
        double = param(
            (
                item,
                '--char_margin 100.0 --boxes_flow 1.0',
                '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3',
            ),
            id=relative_path(item),
            marks=mark.xfail(reason="unsupported font format with current impl")
            if relative_path(item) in UNSUPPORTED_DOCUMENTS else mark.huge)
        result.append(double)
    return result


@fixture(params=params())
def rawresult(request, tmpdir):
    tmpdir = str(tmpdir)
    tocpath = join(tmpdir, 'toc')
    generalpath = join(tmpdir, 'general')
    for item in [tocpath, generalpath]:
        makedirs(item)

    pdf, toccmd, generalcmd = request.param
    rawtoc = 'rawmaker -i %s -o %s --prefix=oneline %s' % (pdf, tocpath, toccmd)
    rawgeneral = 'rawmaker -i %s -o %s %s' % (pdf, generalpath, generalcmd)

    completed = run(rawtoc)
    assert completed.returncode == SUCCESS, str(completed)

    completed = run(rawgeneral)
    assert completed.returncode == SUCCESS, str(completed)

    return (tmpdir, tocpath, generalpath)


@fixture
def sections(rawresult):  # pylint:disable=W0621
    tmpdir, tocpath, generalpath = rawresult

    sectionspath = join(tmpdir, 'sections')
    makedirs(sectionspath)

    runme = 'sections -i %s -i %s -o %s --all'
    runme = runme % (generalpath, tocpath, sectionspath)

    completed = run(runme)
    if completed.returncode != SUCCESS:
        log(completed.stdout)
        log(completed.stderr)
    assert completed.returncode == SUCCESS

    return (tmpdir, tocpath, generalpath, sectionspath)


@fixture
def words(sections):  # pylint:disable=W0621
    tmpdir, tocpath, generalpath, sectionspath = sections

    wordspath = join(tmpdir, 'words')
    makedirs(wordspath)

    runme = 'words -i %s -i %s -o %s --all'
    runme = runme % (generalpath, sectionspath, wordspath)

    completed = run(runme)
    assert completed.returncode == SUCCESS, str(completed)

    # TODO: ADD TEST THAT WORDS WROTE USEFULL THINGS
    return (tmpdir, tocpath, generalpath, sectionspath, wordspath)


@fixture
def groupme(rawresult):  # pylint:disable=W0621
    tmpdir, tocpath, generalpath = rawresult

    groupmepath = join(tmpdir, 'groupme')
    makedirs(groupmepath)

    runme = 'groupme -i %s -i %s -o %s --all'
    runme = runme % (generalpath, tocpath, groupmepath)

    completed = run(runme)
    assert completed.returncode == SUCCESS, str(completed)


@skip_longrun
def test_huge_sections_extractor(testdir, sections):  # pylint:disable=W0621
    assert sections


@skip_longrun
def test_huge_running_words(testdir, words):  # pylint:disable=W0621
    """Run rawmaker -> sections -> words. Ensure that this chain works for
    huge pdf example provided by power tool."""


@skip_longrun
def test_huge_running_groupme(testdir, groupme):  # pylint:disable=W0621
    """Run rawmaker > groupme"""
