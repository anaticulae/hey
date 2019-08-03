# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import basename
from os.path import join

from pytest import fixture
from pytest import param
from utila import SUCCESS
from utila import run
from utila import skip_longrun

from tests import pdfs


def params():
    pdf = pdfs()
    result = []
    for item in pdf:
        # for item in [pdf[0]]:
        double = param(
            (
                item,
                '--char_margin 100.0 --boxes_flow 1.0',
                '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3',
            ),
            id=basename(item),
        )
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
def sections(rawresult):
    tmpdir, tocpath, generalpath = rawresult

    sectionspath = join(tmpdir, 'sections')
    makedirs(sectionspath)

    runme = 'sections -i %s -i %s -o %s --all'
    runme = runme % (generalpath, tocpath, sectionspath)

    completed = run(runme)
    assert completed.returncode == SUCCESS, str(completed)

    return (tmpdir, tocpath, generalpath, sectionspath)


@fixture
def words(sections):
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
def groupme(rawresult):
    tmpdir, tocpath, generalpath = rawresult

    groupmepath = join(tmpdir, 'groupme')
    makedirs(groupmepath)

    runme = 'groupme -i %s -i %s -o %s --all'
    runme = runme % (generalpath, tocpath, groupmepath)

    completed = run(runme)
    assert completed.returncode == SUCCESS, str(completed)


@skip_longrun
def test_huge_sections_extractor(testdir, sections):
    assert sections


@skip_longrun
def test_huge_running_words(testdir, words):
    """Run rawmaker -> sections -> words. Ensure that this chain works for
    huge pdf example provided by power tool."""


@skip_longrun
def test_huge_running_groupme(testdir, groupme):
    """Run rawmaker > groupme"""
