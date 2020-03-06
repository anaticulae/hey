# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Legal Proclamation Parser
=========================

.. code-block:: none

    Eidesstattliche Erklärung


    Hiermit erkläre ich, dass ich die vorliegende Arbeit selbstständig und
    eigenhändig sowie ohne unerlaubte fremde Hilfe und ausschließlich unter
    Verwendung der aufgeführten Quellen und Hilfsmittel angefertigt habe.


    ------------ --------------
    (Ort, Datum) (Unterschrift)

Special Marks
-------------

Word Groups:

* Eidesstattliche Erklärung
* Selbstständigkeitserklärung
* angefertigt
* aufgeführten Quellen und Hilfsmittel
* ausschließlich
* diese Arbeit
* eigenhändig
* erkläre ich
* fremden Quellen wörtlich
* gleicher oder ähnlicher Form
* hiermit erkläre ich
* selbstständig
* sinngemäß entnommen
* versichere ich
* vorliegende Arbeit

Notes:

* Ort
* Datum
* Unterschrift

Requirements
------------

* do not add to page count
* do not add to table of content

[Theisen]
"""

import texmex
import utila

import sections.utils.spa


def work(document: str, position: str, pages=None) -> str:
    data = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
    )

    config = sections.utils.spa.Config(
        likelihood_name='legal',
        page_analysis=analyse_page,
    )

    dumped = sections.utils.spa.work(
        data=data,
        config=config,
    )

    return dumped


FEATURE_POINTS = [
    'Datum',
    'Eidesstattliche Erklärung',
    'Ort',
    'Selbstständigkeitserklärung',
    'Unterschrift',
    'angefertigt',
    'aufgeführten Quellen und Hilfsmittel',
    'ausschließlich',
    'diese Arbeit',
    'eigenhändig',
    'erkläre ich',
    'fremden Quellen wörtlich',
    'gleicher oder ähnlicher Form',
    'hiermit erkläre ich',
    'selbstständig',
    'sinngemäß entnommen',
    'versichere ich',
    'vorliegende Arbeit',
    'Arbeit',
]

MIN_FEATURE_POINT_COUNT = 5  # TODO: HOLY VALUE


def analyse_page(navigator: texmex.PageTextNavigator
                ) -> sections.feature.StatisticalResultItem:
    # TODO: REPLACE AFTER UPGRADING TEXMEX
    raw = utila.NEWLINE.join([item.text for item in navigator])

    located = [item for item in FEATURE_POINTS if item.lower() in raw.lower()]

    trust = 0.0
    if 'Eidesstattliche Erklärung' in raw:
        trust += 0.5
    if 'Selbstständigkeitserklärung' in raw:
        trust += 0.5

    feature_point_count = len(located)
    if feature_point_count >= MIN_FEATURE_POINT_COUNT:
        trust += 0.25
    if feature_point_count > 8:
        trust += 0.5

    if feature_point_count < MIN_FEATURE_POINT_COUNT:
        feature_point_count = 0
        trust = 0.0
    return len(located), trust
