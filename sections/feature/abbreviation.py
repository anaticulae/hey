# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Likelihood Detection
=================================

Currently there are two different approaches to differentiate between
abbreviation and non abbreviation pages. On the first side we check that
there are not to much sentences on a page. On the other side we search
for selective words "Abkuerzungsverzeichnis, ...".

NOTE: This approach is only for demo time.
"""

import texmex

import sections.feature
import sections.utils.spa
import sections.utils.text

TITLE = ['Abkürzungsverzeichnis']


def work(document: str, position: str, pages=None) -> str:
    data = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
    )

    config = sections.utils.spa.Config(
        likelihood_name='abbrviation_table',
        page_analysis=analyse_page,
    )

    dumped = sections.utils.spa.work(
        data=data,
        config=config,
    )

    return dumped


def analyse_page(navigator: texmex.PageTextNavigator
                ) -> sections.feature.StatisticalResultItem:
    result = []
    if not is_abbreviation_table_statistical(navigator):
        return (0, 0.0)

    for line in navigator:
        line = line.text.strip()
        if line in TITLE:
            result.append(line)

    if not result:
        # could not find any TITLE line
        return (0, 0)
    return (len(result), 1.0)


def is_abbreviation_table_statistical(navigator: texmex.PageTextNavigator):
    textonpage = sections.utils.text.textonpage(navigator)
    if len(textonpage.sentences) > 5:
        # TODO: HOLY VALUE
        return False
    return True
