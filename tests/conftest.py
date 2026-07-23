# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import gennex
import hoverpower
import utilo
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import hey
import tests

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = hey.PACKAGE
hoverpower.setup(hey.ROOT)

RESOURCES = [
    hoverpower.DISS266_PDF,
    hoverpower.DISS205_PDF,
    hoverpower.todo(
        hoverpower.MASTER116_PDF,
        caption=True,
        cleanup=True,
        codero=True,
        figureo=True,
        footnote=True,
        groupme=True,
        headnote=True,
        magic=True,
        pagenumber=True,
        tablero=True,
    ),
    hoverpower.BACHELOR111_PDF,
    hoverpower.MASTER099_PDF,
    hoverpower.MASTER098_PDF,
    hoverpower.todo(
        hoverpower.BACHELOR090_PDF,
        caption=True,
        cleanup=True,
        codero=True,
        figureo=True,
        footnote=True,
        groupme=True,
        headnote=True,
        magic=True,
        pagenumber=True,
        tablero=True,
    ),
    hoverpower.MASTER072_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR056_PDF,
    hoverpower.HOME025_PDF,
    hoverpower.DOCU007_PDF,
    hoverpower.MASTER031_PDF,
    (hoverpower.MASTER110_PDF, '0:60'),
]

WORKER = utilotest.worker_count(5, onci=len(RESOURCES))


# def pytest_sessionstart(session):  # pylint:disable=W0613
    # hoverpower.run()


# TODO: ENABLE LATER
# def extract(resources):
#     gennex.extract(
#         resources,
#         #cleanup=True,
#         codero=True,
#         figureo=True,
#         footnote=True,
#         groupme=True,
#         headnote=True,
#         magic=True,
#         pagenumber=True,
#         tablero=True,
#         worker=WORKER,
#     )


RESOURCES_SECTIONSANDWORDS = [
    (hoverpower.MASTER072_PDF, '0:16'),
    (hoverpower.BACHELOR128_PDF, '0:50'),
]

# TODO: ENABLE LATER
# def extract_sectionsandwords(resources):
#     dest = hoverpower.generated(folder='sectionsandwords')
#     gennex.extract(
#         resources,
#         dest=dest,
#         caption=True,
#         cleanup=True,
#         detector=True,
#         headnote=True,
#         footnote=True,
#         groupme=True,
#         headlines=True,
#         lists=True,
#         magic=True,
#         pagenumber=True,
#         sections=True,
#         spacestation=True,
#         tablero=False,  # reduce generation time
#         textflow=True,
#         words=True,
#     )


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
        tmp = utilo.tmpfile(hoverpower.ROOT)
        utilo.file_replace(tmp, script)
        utilo.run(f'jam -i {source} --script {tmp} -o {outpath}')
    # run rawmaker
    resources = [
        tests.LINEDISTANCE100_PDF,
        tests.LINEDISTANCE150_PDF,
        tests.LINEDISTANCE200_PDF,
    ]
    gennex.extract(
        resources,
        dest=dest,
        base=dest,
        groupme=True,
        footnote=True,
        headnote=True,
        pagenumber=True,
    )


def validate_linedistances(_):  # pylint:disable=W0613
    # disable page number validation
    pass
