# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import hey
import hey.example

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = hey.PACKAGE

RESOURCES = [
    power.MASTER116_PDF,
    power.BACHELOR111_PDF,
    power.MASTER099_PDF,
    power.MASTER098_PDF,
    power.BACHELOR090_PDF,
    power.MASTER072_PDF,
    power.BACHELOR063_PDF,
    (power.BACHELOR056_PDF, '0:55'),
    power.HOMEWORK025_PDF,
    (power.MASTER089_PDF, '78:85'),
    power.DOCU07_PDF,
]

WORKER = 4


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


def extract(resources):
    destination = power.generated()

    hey.example.extract(
        resources + [power.REPOSITORY],
        destination=destination,
        groupme=True,
        worker=WORKER,
        pages=':',
    )


RESOURCES_SECTIONSANDWORDS = [
    (power.MASTER072_PDF, '0:16'),
]


def extract_sectionsandwords(resources):
    destination = power.generated(folder='sectionsandwords')
    hey.example.extract(
        resources + [power.REPOSITORY],
        destination=destination,
        caption=True,
        detector=True,
        groupme=True,
        sections=True,
        textflow=True,
        words=True,
        pages=':',
    )
