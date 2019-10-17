# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import groupme.footer.fixed
import tests.resources
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_horizontals


def test_groupme_footer_fixed_extract(restructured_horizontals):  #pylint:disable=W0621
    horizontals = restructured_horizontals

    sizeandborder = tests.resources.sizeandborder(tests.resources.BACHELOR_111PAGES)  #yapf:disable
    sizeandborder = serializeraw.load_pageborders(sizeandborder)
    pageheight = utila.select_page(sizeandborder, 0).size.height

    top, bottom = groupme.footer.fixed.extract_common_footer(
        horizontals=horizontals,
        pageheight=pageheight,
    )
    assert top  # document has header
    assert bottom  # document has footer

    assert top < bottom


def test_groupme_footer_fixed_bachelor111page():
    horizontals = tests.resources.horizontals(tests.resources.BACHELOR_111PAGES)
    horizontals = serializeraw.load_horizontals(horizontals)

    sizeandborder = tests.resources.sizeandborder(tests.resources.BACHELOR_111PAGES)  #yapf:disable
    sizeandborder = serializeraw.load_pageborders(sizeandborder)
    pageheight = utila.select_page(sizeandborder, 0).size.height

    top, bottom = groupme.footer.fixed.extract_common_footer(
        horizontals=horizontals,
        pageheight=pageheight,
    )
    assert top  # document has header
    assert bottom  # document has footer
    assert top < bottom
