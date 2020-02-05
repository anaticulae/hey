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


def install_requirements():
    utila.clean_install(hey.ROOT, hey.PACKAGE)


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


PACKAGE = [
    (tests.resources.BACHELOR111_PDF, tests.resources.BACHELOR111),
    (tests.resources.HOWTO_ARGPARSE_PDF, tests.resources.HOWTO_ARGPARSE),
    (tests.resources.MASTER72_PDF, tests.resources.MASTER72),
    (tests.resources.PYPORTING_PDF, tests.resources.PYPORTING),
    (tests.resources.RESTRUCT_PDF, tests.resources.RESTRUCT),
    (tests.resources.SIMPLE_PDF, tests.resources.SIMPLE),
    (tests.resources.TECHNICAL24_PDF, tests.resources.TECHNICAL24),
    (tests.resources.TWINE_PDF, tests.resources.TWINE),
]


def run_package(pdf, outpath):
    utila.log(f'run {pdf}')
    todo = []
    todo.extend(create_todo_rawmaker(pdf, outpath))
    todo.extend(create_todo_groupme(outpath))
    todo.extend(create_todo_sections(outpath))

    todo = [
        f'{executable} -i {inpath} -o {outpath} {configuration}'
        for (executable, inpath, outpath, configuration) in todo
    ]
    todo = ' && '.join(todo)  # pylint:disable=R0204
    completed = utila.run(todo)
    utila.assert_success(completed)
    return todo


WORKER = 8


def extract_examples():
    if os.path.exists(tests.resources.GENERATED):
        return

    extract_standard()
    extract_without_titlepage()
    extract_single()


def run_single(pdf, dest):
    todo = create_todo_rawmaker(pdf, dest)
    todo = [
        f'{executable} -i {inpath} -o {outpath} {configuration}'
        for (executable, inpath, outpath, configuration) in todo
    ]
    todo = ' && '.join(todo)  # pylint:disable=R0204
    completed = utila.run(todo)
    utila.assert_success(completed)
    return todo


def extract_single():
    plan = [
        (
            tests.resources.BACHELOR56_PDF,
            tests.resources.BACHELOR56,
        ),
        (tests.resources.MASTER89_PDF, tests.resources.MASTER89),
        (
            tests.resources.HOWTOWRITE9_PDF,
            tests.resources.HOWTOWRITE9,
        ),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        futures = {
            executor.submit(run_single, pdf, out): pdf for pdf, out in plan
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception:
                utila.info(f'{future} failed.')
                raise


def extract_standard():
    for pdf, _ in PACKAGE:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), pdf

    # ensure that generation directory exists
    os.makedirs(tests.resources.GENERATED)

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        futures = {
            executor.submit(run_package, pdf, out): pdf for pdf, out in PACKAGE
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception:
                utila.info(f'{future} failed.')
                raise


def create_todo_rawmaker(inpath, outpath):
    result = [
        (
            'rawmaker -j8',
            inpath,
            outpath,
            detector.feature.titlepage.RAWMAKER_CONFIGURATION,
        ),
        (
            'rawmaker -j8',
            inpath,
            outpath,
            '--all --char_margin=5.0 --boxes_flow=1.0 --line_margin=0.3',
        ),
        # TODO: move configuration to global var
    ]
    return result


def create_todo_sections(path):
    result = [
        ('sections', path, path, '--all'),
    ]
    return result


def create_todo_groupme(path):
    result = [
        ('groupme', path, path, ''),
    ]
    return result


def extract_without_titlepage():
    destination = tests.resources.NO_TITLE
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in hey.example.output_names(tests.resources.NO_TITLE_EXAMPLE)
    ]
    for inpath, outpath in zip(
            tests.resources.NO_TITLE_EXAMPLE,
            without_titlepage,
    ):
        completed = utila.run(f'jam -i {inpath} -o {outpath} --remove=0')
        assert completed.returncode == utila.SUCCESS, str(completed)

    hey.example.extract(without_titlepage, destination, pages='0:20')
