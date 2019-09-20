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


def extract_examples():
    if os.path.exists(tests.resources.GENERATED):
        return
    os.makedirs(tests.resources.GENERATED)

    todo = create_todo_rawmaker(
        'master/page_72_noimages_toc.pdf',
        tests.resources.MASTER_72PAGES,
    ) + create_todo_rawmaker(
        'restruct/restructuredtext.pdf',
                tests.resources.RESTRUCT,
    ) + create_todo_rawmaker(
        'porting_module/porting_module_to_python3.pdf',
                tests.resources.PYPORTING,
    ) + create_todo_rawmaker(
        'simple/howto_pyporting.pdf',
        tests.resources.SIMPLE,
    ) + create_todo_sections(tests.resources.RESTRUCT) \
      + create_todo_sections(tests.resources.SIMPLE)\
      + create_todo_sections(tests.resources.PYPORTING)

    for (executable, inpath, outpath, configuration) in todo:
        cmd = f'{executable} -i {inpath} -o {outpath} {configuration}'
        utila.debug(f'run {cmd}')
        completed = utila.run(cmd, cwd=tests.resources.RESOURCES)
        assert completed.returncode == utila.SUCCESS, str(completed)
        utila.debug('completed')


def create_todo_rawmaker(inpath, outpath):
    result = [
        (
            'rawmaker',
            inpath,
            outpath,
            detector.feature.titlepage.RAWMAKER_CONFIGURATION,
        ),
        (
            'rawmaker',
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
