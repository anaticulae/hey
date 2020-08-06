# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import groupme.border.leftright
import groupme.serialize
import tests.groupme_


def load_example(path: str):
    # TODO: USE ONELINE?
    textpositions = serializeraw.load_textpositions(path)
    pagesizes = serializeraw.load_pageborders(path)
    return textpositions, pagesizes


def load_leftright(path: str):
    textpositions, pagesizes = load_example(path)
    left, right = groupme.border.leftright.determine_pageborder(
        textpositions,
        pagesizes,
    )
    return left, right


def test_leftright_run():
    """Detect book-like document with different border for left and
    right page."""
    left, right = load_leftright(power.link(power.BOOK007_PDF))
    result = groupme.border.leftright.simple(left, right)
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


def test_leftright_run_noleftright():
    """Ensure that document with single page layout has no different
    border for left and right but only a single border."""
    textpositions, pagesizes = load_example(power.link(power.MASTER072_PDF))
    result = groupme.border.leftright.run(textpositions, pagesizes)
    assert result.valid is False, result
    # ensure that left border is more left then right
    assert result.left < result.right, result


def test_leftright_one_error():
    """Introduce error to challenge algorithm."""
    left, right = load_leftright(power.link(power.BOOK007_PDF))

    left.append(left.pop(3))
    right.append(right.pop(3))

    result = groupme.border.leftright.raising(left, right)
    assert result, result
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


def test_leftright_raising_bachelor241():
    left, right = load_leftright(power.link(power.BACHELOR241_PDF))
    result = groupme.border.leftright.raising(left, right)
    assert result, result
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


def test_leftright_strategy_witherror():
    """Run left right strategy with example which contains an error."""
    textpositions, pagesizes = load_example(power.link(power.BOOK007_PDF))

    textpositions, pagesizes = introduce_error(textpositions, pagesizes)

    result = groupme.border.leftright.run(textpositions, pagesizes)
    assert result, result
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


def test_leftright_bachelor241(testdir, monkeypatch):
    """Regression test to ensure that bachelor241 border is detected
    correctly."""
    source = power.link(power.BACHELOR241_PDF)
    tests.groupme_.run(f'-i {source} --border', monkeypatch=monkeypatch)

    leftright = groupme.serialize.load_leftright_border(testdir.tmpdir)
    assert leftright[0] != leftright[1]


def introduce_error(left, right):
    left, right = left[:], right[:]
    # introduce an error
    left.append(left.pop(3))
    right.append(right.pop(3))

    lresult, rresult = [], []
    # fix page number - ensure to have ascending page numbers
    for page, (first, second) in enumerate(zip(left, right)):
        lresult.append(first._replace(page=page))  # pylint:disable=W0212
        rresult.append(second._replace(page=page))  # pylint:disable=W0212
    return lresult, rresult
