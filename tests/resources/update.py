# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

from hey import ROOT
from tests.resources import RESOURCES


def install_requirements():
    utila.clean_install(ROOT, 'hey')


def sync_resources():
    completed = utila.run('power --all', RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    todo = create_todo_rawmaker(
        'restruct/restructuredtext.pdf',
        './restruct',
    ) + create_todo_rawmaker(
        'porting_module/porting_module_to_python3.pdf',
        './porting_module',
    ) + create_todo_rawmaker(
        'simple/howto_pyporting.pdf',
        './simple',
    ) + create_todo_sections('./restruct') + create_todo_sections(
        './simple') + create_todo_sections('./porting_module')

    for (executable, inpath, outpath, configuration) in todo:
        cmd = f'{executable} -i {inpath} -o {outpath} {configuration}'
        utila.debug(f'run {cmd}')
        completed = utila.run(cmd, cwd=RESOURCES)
        assert completed.returncode == utila.SUCCESS, str(completed)
        utila.debug('completed')


def create_todo_rawmaker(inpath, outpath):
    result = [
        (
            'rawmaker',
            inpath,
            outpath,
            ('--prefix=oneline '
             '--font --text --toc '
             '--char_margin=100.0 --boxes_flow=1.0'),
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
