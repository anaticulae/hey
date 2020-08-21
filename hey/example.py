# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Test-Data-Generator
===================

The purpose of this test-data-generator is to deliver easy use test data
for following analysis steps. Furthermore these examples shows how to
use the different tools together. We do not want to duplicate any
generator code.
"""

import concurrent.futures
import os
import os.path

import utila
import utilatest

ONELINE = ('--prefix=oneline '
           '--font --text '
           '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001')

CONFIG = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25 '


def extract(  # pylint:disable=R0914
        files: list,
        destination: str,
        pages: str = '0:10',
        worker: int = 12,
        rawmaker: str = CONFIG,
        oneline: str = ONELINE,
        *,
        caption: bool = False,
        detector: bool = False,
        doctextstyle: bool = False,
        groupme: bool = False,
        magic: bool = False,
        sections: bool = False,
        textflow: bool = False,
        words: bool = False,
        full: bool = False,
):
    """Run rawmaker, groupme, sections and words for given `files` and write
    result to `destination`.

    Args:
        files(list): list of files to work on; list of pattern
                     (file, _pages_) or (file). If `_pages_` is given
                     use default var `pages`.
        destination(path): create folder for every file and save result
        pages(str): range of selected pages
        worker(int): number of threads to extract examples
        rawmaker(str): default config
        oneline(str): oneline config
        caption(bool): run if True
        detector(bool): run if True
        doctextstyle(bool): run if True
        groupme(bool): run if True
        magic(bool): run if True
        sections(bool): run if True
        textflow(bool): run if True
        words(bool): run if True
        full(bool): overwrites every selection and runs all extraction steps
    Raises:
        Exception: if Exception occurs while extracting file
    """
    todo = todolist(
        files,
        destination,
        pages,
        rawmaker=rawmaker,
        oneline=oneline,
        caption=caption,
        detector=detector,
        doctextstyle=doctextstyle,
        groupme=groupme,
        magic=magic,
        sections=sections,
        textflow=textflow,
        words=words,
        full=full,
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = [executor.submit(run_job, job) for job in todo]
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception:
                utila.info(f'{future} failed.')
                raise


def todolist(  # pylint:disable=R0914
        files: list,
        destination: str,
        pages: str = '0:10',
        rawmaker: str = CONFIG,
        oneline: str = ONELINE,
        *,
        caption: bool = False,
        detector: bool = False,
        doctextstyle: bool = False,
        groupme: bool = False,
        magic: bool = False,
        sections: bool = False,
        textflow: bool = False,
        words: bool = False,
        full: bool = False,
):
    """Create todo list to extract resources.

        files: list of resources to extract. There are two list pattens:
               (file, pages) or (file).
        full: overwrites every selection and runs all extraction steps
    """
    if full:
        # enable every extraction step
        caption = True
        detector = True
        doctextstyle = True
        groupme = True
        magic = True
        sections = True
        textflow = True
        words = True

    config = {
        'caption': caption,
        'detector': detector,
        'doctextstyle': doctextstyle,
        'groupme': groupme,
        'magic': magic,
        'sections': sections,
        'textflow': textflow,
        'words': words,
    }
    todo = generate(
        files,
        destination,
        pages=pages,
        config=config,
        rawmaker=rawmaker,
        oneline=oneline,
    )
    return todo


def run_job(job: str):
    utila.log(f'start: {job[0:200]}')
    completed = utila.run(job)
    utila.assert_success(completed)
    utila.log(f'completed: {job[0:100]}')


def generate(
        files: list,
        outpath: str,
        pages: str,
        config: dict,
        rawmaker: str,
        oneline: str,
) -> list:
    todo = []
    single_pages = paged(files, default=pages)
    files = list(single_pages.keys())
    names = utilatest.simplify_testfile_names(files, sort=False)
    for inpath, output in zip(files, names):
        next_job = create_job(
            inpath,
            os.path.join(outpath, output),
            pages=single_pages[inpath],
            config=config,
            rawmaker=rawmaker,
            oneline=oneline,
        )
        todo.append(next_job)
    return todo


def paged(files, default=None) -> dict:
    """Select pages, if given `(source, pages)`, to extract. If no pages
    are given, use `default` one."""
    result = {}
    for item in files:
        page = default
        if isinstance(item, tuple):
            item, page = item
        result[item] = page
    return result


def create_job(
        src: str,
        dest: str,
        rawmaker: str,
        oneline: str,
        pages: tuple = None,
        config: dict = None,
) -> str:
    """Create job to run required steps for next processing unit.

    Args:
        src: pdf file for processing
        dest: output path to output folder
        rawmaker: default config
        oneline: default oneline config
        pages: shrink processing if given - if None process all pages
        config: select which processes to run
    Returns:
        Created process todo description.
    """
    if config is None:
        config = {}

    pages = f'--pages={pages}' if pages is not None else ''
    task = [
        f'rawmaker -j=auto -i {src} -o {dest} {rawmaker} {pages}',
        f'rawmaker -j=auto -i {src} -o {dest} {oneline} {pages}',
        f'linero -i {dest} -o {dest}',
    ]
    if config.get('groupme', False):
        # run all, disable --toc
        task.append(f'groupme --toc! -j=auto -i {dest} -o {dest}')
        # toc only
        task.append(f'groupme --toc --pages=0:10 -i {dest} -o {dest}')
    if config.get('sections', False):
        task.append(f'sections -j=auto -i {dest} -o {dest}')
    if config.get('words', False):
        task.append(f'words -j=auto -i {dest} -o {dest}')
    if config.get('detector', False):
        task.append(f'detector -i {dest} -o {dest}')
    if config.get('textflow', False):
        task.append(f'textflow -i {dest} -o {dest}')
    if config.get('doctextstyle', False):
        task.append(f'doctextstyle -i {dest} -o {dest}')
    if config.get('caption', False):
        task.append(f'caption -i {dest} -o {dest}')
    if config.get('magic', False):
        task.append(f'magic -i {dest} -o {dest}')
    todo = ' && '.join(task)
    return todo
