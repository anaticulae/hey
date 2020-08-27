# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import hey
import hey.example
import tests.resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = hey.PACKAGE

RESOURCES = [
    power.MASTER116_PDF,
    power.MASTER099_PDF,
    power.MASTER098_PDF,
    power.BACHELOR090_PDF,
    power.BACHELOR241_PDF,
    power.HOMEWORK018_PDF,
    (power.DISS264_PDF, '0:50'),
    (power.BACHELOR056_PDF, '0:55'),
    (power.MASTER089_PDF, '0:89'),
    power.BACHELOR076_PDF,
    power.MASTER072_PDF,
    power.BACHELOR111_PDF,
    power.BACHELOR037_PDF,
    (power.BACHELOR063_PDF, '0:9,59:62'),
    power.HOMEWORK025_PDF,
    power.DOCU27_PDF,
    power.TECHNICAL_024,
    power.DOCU14_PDF,
    power.DOCU07_PDF,
    power.BOOK007_PDF,
    power.DOCU09_PDF,
    power.DOCU35_PDF,
    (power.HOMEWORK050_PDF, '0:10'),
    (power.ORDER009_PDF, '0:10'),
    (power.MASTER078_PDF, '0:5'),
    (power.MASTER083_PDF, '0:10'),
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


RESOURCES_NOTITLE = tests.resources.NO_TITLE_EXAMPLE


def extract_notitle(resources):
    destination = power.generated(folder='notitle')
    files = [item[0] if isinstance(item, tuple) else item for item in resources]
    # prepare
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in utilatest.simplify_testfile_names(
            files + [power.REPOSITORY],  # ensure correct parent
            sort=False,
        )
    ]
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        todo.append(f'jam -i {inpath} -o {outpath} --remove=0')
    utila.run_parallel(todo)

    # generate
    hey.example.extract(
        without_titlepage + [destination],  # ensure correct parent
        destination,
        groupme=True,
        pages='0:10',
        worker=1,
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
