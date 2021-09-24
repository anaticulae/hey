# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import genex
import power
import utila

import hey
import tests

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = hey.PACKAGE
power.setup(hey.ROOT)

RESOURCES = [
    power.DISS266_PDF,
    power.DISS205_PDF,
    power.MASTER116_PDF,
    power.BACHELOR111_PDF,
    power.MASTER099_PDF,
    power.MASTER098_PDF,
    power.BACHELOR090_PDF,
    power.MASTER072_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR056_PDF,
    power.HOME025_PDF,
    power.DOCU007_PDF,
    (power.MASTER110_PDF, '0:60'),
]

WORKER = 4


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


def extract(resources):
    destination = power.generated()
    genex.extract(
        resources,
        destination=destination,
        groupme=True,
        magic=True,
        codero=True,
        figureo=True,
        tablero=True,
        worker=WORKER,
        pages=':',
        base=power.REPOSITORY,
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
        magic=True,
        sections=True,
        spacestation=True,
        textflow=True,
        words=True,
        tablero=False,  # reduce generation time
        pages=':',
    )


RESOURCES_LINEDISTANCES = [
    (tests.LINEDISTANCE_PDF, ('sel page_0.text_5_450', 'percent200')),
    (tests.LINEDISTANCE_PDF, ('sel page_0.text_450_940', 'percent150')),
    (tests.LINEDISTANCE_PDF, ('sel page_0.text_940_1450', 'percent100')),
]


def extract_linedistances(resources):
    dest = tests.LINESGENERATED
    if os.path.exists(dest):
        return
    os.makedirs(dest)
    for source, (script, name) in resources:
        outpath = os.path.join(dest, f'{name}.pdf')
        tmp = utila.tmpfile(power.ROOT)
        utila.file_replace(tmp, script)
        utila.run(f'jam -i {source} --script {tmp} -o {outpath}')
    # run rawmaker
    resources = [
        tests.LINEDISTANCE100_PDF,
        tests.LINEDISTANCE150_PDF,
        tests.LINEDISTANCE200_PDF,
    ]
    genex.extract(
        resources,
        destination=dest,
        base=dest,
        pages=':',
        groupme=True,
        tablero=False,  # reduce generation time
    )


def validate_linedistances(_):  # pylint:disable=W0613
    # disable page number validation
    pass
