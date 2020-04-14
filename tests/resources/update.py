# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import os

import utila

import detector
import detector.feature.titlepage
import hey
import hey.example
import tests.resources

WORKER = 12


def install_requirements():
    utila.clean_install(hey.ROOT, hey.PACKAGE)


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    if os.path.exists(tests.resources.GENERATED):
        return
    extract()
    extract_without_titlepage()


CONFIG = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25 '
ONELINE = detector.feature.titlepage.RAWMAKER_CONFIGURATION

PACKAGE = [
    (tests.resources.BACHELOR111_PDF, tests.resources.BACHELOR111, None),
    (tests.resources.BACHELOR37_PDF, tests.resources.BACHELOR37, '0:30'),
    (tests.resources.BACHELOR63_PDF, tests.resources.BACHELOR63, '0:9,59:62'),
    (tests.resources.HOWTO_ARGPARSE_PDF, tests.resources.HOWTO_ARGPARSE, None),
    (tests.resources.HOWTO_PYPORTING_PDF, tests.resources.HOWTO_PYPORTING,
     None),
    (tests.resources.LEFTRIGHT_PDF, tests.resources.LEFTRIGHT, None),
    (tests.resources.MASTER72_PDF, tests.resources.MASTER72, None),
    (tests.resources.PYPORTING_PDF, tests.resources.PYPORTING, None),
    (tests.resources.RESTRUCT_PDF, tests.resources.RESTRUCT, None),
    (tests.resources.TECHNICAL24_PDF, tests.resources.TECHNICAL24, None),
    (tests.resources.TWINE_PDF, tests.resources.TWINE, None),
    (tests.resources.BACHELOR56_PDF, tests.resources.BACHELOR56, '0:55'),
    (tests.resources.HOMEWORK50_PDF, tests.resources.HOMEWORK50, '6'),
    (tests.resources.HOWTOWRITE9_PDF, tests.resources.HOWTOWRITE9, '0:10'),
    (tests.resources.MASTER116_PDF, tests.resources.MASTER116, '0:5,96:101'),
    (tests.resources.MASTER89_PDF, tests.resources.MASTER89, '0:89'),
]


def run_package(pdf, outpath, pages=None):
    relative = utila.make_relative(pdf, tests.resources.RESOURCES)
    utila.log(f'run: {relative}')
    todo = create_todo(pdf, outpath, pages=pages)
    for item in todo:
        if isinstance(item, str):
            completed = utila.run(item)
            utila.assert_success(completed)
        else:
            parallel = [
                ' && '.join(sequence)
                if isinstance(sequence, tuple) else sequence
                for sequence in item
            ]
            ret = utila.run_parallel(parallel)
            assert ret == utila.SUCCESS, str(parallel)
    utila.log(f'completed: {relative}')


def extract():
    for pdf, _, __ in PACKAGE:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), pdf

    # ensure that generation directory exists
    os.makedirs(tests.resources.GENERATED)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        futures = {
            executor.submit(run_package, pdf, out, pages=pages): pdf
            for pdf, out, pages in PACKAGE
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as error:  # pylint:disable=broad-except
                utila.error(f'{future} failed.')
                utila.error(error)


def create_todo(inpath, outpath, pages: tuple = None):
    pages = f' --pages {pages} ' if pages is not None else ' '
    result = (
        (
            (
                f'rawmaker -j8 -i {inpath} -o {outpath} {CONFIG} {pages}',
                f'linero -i {outpath} -o {outpath}',
            ),
            f'rawmaker -j8 -i {inpath} -o {outpath} {ONELINE} {pages}',
        ),
        f'groupme -j8 -i {outpath} -o {outpath} {pages}',
    )
    return result


def extract_without_titlepage():
    destination = tests.resources.NO_TITLE
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf') for item in
        utila.simplify_testfile_names(tests.resources.NO_TITLE_EXAMPLE)
    ]
    todo = [
        f'jam -i {inpath} -o {outpath} --remove=0' for inpath, outpath in zip(
            tests.resources.NO_TITLE_EXAMPLE,
            without_titlepage,
        )
    ]
    returncode = utila.run_parallel(todo, worker=WORKER)
    assert returncode == utila.SUCCESS, str(returncode)
    hey.example.extract(
        files=without_titlepage,
        destination=destination,
        pages='0:10',
        detector=False,
        sections=False,
        words=False,
    )
