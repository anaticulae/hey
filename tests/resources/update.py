# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import detector.feature.titlepage
import hey
import tests.resources


def install_requirements():
    utila.clean_install(hey.ROOT, hey.PACKAGE)


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


RAWMAKER = [
    (
        tests.resources.RESTRUCT_PDF,
        tests.resources.RESTRUCT,
    ),
    (
        tests.resources.HOWTO_ARGPARSE_PDF,
        tests.resources.HOWTO_ARGPARSE,
    ),
    (
        tests.resources.PYPORTING_PDF,
        tests.resources.PYPORTING,
    ),
    (
        tests.resources.SIMPLE_PDF,
        tests.resources.SIMPLE,
    ),
    (
        tests.resources.MASTER_72PAGES_PDF,
        tests.resources.MASTER_72PAGES,
    ),
]

SECTION = [
    tests.resources.MASTER_72PAGES,
    tests.resources.PYPORTING,
    tests.resources.RESTRUCT,
    tests.resources.SIMPLE,
]


def extract_examples():
    if os.path.exists(tests.resources.GENERATED):
        return
    os.makedirs(tests.resources.GENERATED)

    todo = []
    for pdf, out in RAWMAKER:
        todo.extend(create_todo_rawmaker(pdf, out))
    for path in SECTION:
        todo.extend(create_todo_sections(path))

    for (executable, inpath, outpath, configuration) in todo:
        cmd = f'{executable} -i {inpath} -o {outpath} {configuration}'
        utila.debug(f'run {cmd}')
        completed = utila.run(cmd, cwd=tests.resources.RESOURCES)
        utila.assert_success(completed)
        utila.debug('completed')


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
            ('--border --boxes --font --text --toc '
             '--char_margin=5.0 --boxes_flow=1.0 --line_margin=0.3'),
        ),
    ]
    return result


def create_todo_sections(path):
    result = [
        (
            'sections',
            path,
            path,
            '--chapter --index --sections --title --toc --whitepage',
        ),
    ]
    return result
