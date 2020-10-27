# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power

import hey

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = hey.PACKAGE
power.setup(hey.ROOT)

RESOURCES = [
    power.MASTER116_PDF,
    power.BACHELOR111_PDF,
    power.MASTER099_PDF,
    power.MASTER098_PDF,
    power.BACHELOR090_PDF,
    power.MASTER072_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR051_PDF,
    (power.BACHELOR056_PDF, '0:55'),
    power.HOME025_PDF,
    (power.MASTER089_PDF, '78:85'),
    power.DOCU07_PDF,
    (power.MASTER110_PDF, '0:60'),
]

WORKER = 4


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


def extract(resources):
    destination = power.generated()

    genex.extract(
        resources + [power.REPOSITORY],
        destination=destination,
        groupme=True,
        magic=True,
        worker=WORKER,
        pages=':',
    )


RESOURCES_SECTIONSANDWORDS = [
    (power.MASTER072_PDF, '0:16'),
    (power.BACHELOR128_PDF, '0:50'),
]


def extract_sectionsandwords(resources):
    destination = power.generated(folder='sectionsandwords')
    genex.extract(
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
