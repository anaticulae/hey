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

import detector.feature.titlepage as dft


def extract(  # pylint:disable=R0914
        files: list,
        destination: str,
        pages: str = '0:10',
        worker: int = 12,
        *,
        groupme: bool = True,
        sections: bool = True,
        words: bool = True,
        detector: bool = True,
):
    """Run rawmaker, groupme, sections and words for given `files` and write
    result to `destination`.

    Args:
        files(list): list of files to work on
        destination(path): create folder for every file and save result
        pages(str): range of selected pages
        worker(int): number of threads to extract examples
        groupme(bool): run if True
        sections(bool): run if True
        words(bool): run if True
        detector(bool): run if True
    Raises:
        Exception: if Exception occurs while extracting file
    """
    for pdf in files:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), str(pdf)

    # ensure that generation directory exists
    os.makedirs(destination, exist_ok=True)

    def run_job(job: str):
        completed = utila.run(job)
        utila.assert_success(completed)

    config = {
        'groupme': groupme,
        'sections': sections,
        'words': words,
        'detector': detector,
    }
    generated = generate(files, destination, pages=pages, config=config)

    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = {executor.submit(run_job, pdf): pdf for pdf in generated}
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception:
                utila.info(f'{future} failed.')
                raise


def generate(files: list, outpath: str, pages: str, config: dict) -> list:
    todo = []
    names = output_names(files)
    for inpath, output in zip(files, names):
        next_job = create_job(
            inpath,
            os.path.join(outpath, output),
            pages=pages,
            config=config,
        )
        todo.append(next_job)
    return todo


def create_job(
        src: str,
        dest: str,
        pages: tuple = None,
        config: dict = None,
) -> str:
    """Create job to run required steps for next processing unit.

    Args:
        src: pdf file for processing
        dest: output path to output folder
        pages: shrink processing if given - if None process all pages
        config: select which processes to run
    Returns:
        Created process todo description.
    """
    assert os.path.exists(src), str(src)
    if config is None:
        config = {}

    oneline = dft.RAWMAKER_CONFIGURATION
    # TODO: USE A MORE GENERAL PLACE
    layoutconfig = '--all --char_margin=5.0 --boxes_flow=1.0 --line_margin=0.3'

    pages = f'--pages={pages}' if pages is not None else ''
    task = [
        f'rawmaker -j 8 -i {src} -o {dest} {layoutconfig} {pages}',
        f'rawmaker -j 8 -i {src} -o {dest} {oneline} {pages}',
        f'linero -i {dest} -o {dest}',
    ]
    if config.get('groupme', False):
        task.append(f'groupme -j 8 -i {dest} -o {dest}')
    if config.get('sections', False):
        task.append(f'sections -j 8 -i {dest} -o {dest}')
    if config.get('words', False):
        task.append(f'words -j 8 -i {dest} -o {dest}')
    if config.get('detector', False):
        task.append(f'detector -i {dest} -o {dest}')
    todo = ' && '.join(task)
    return todo


def output_names(files):
    files = [utila.forward_slash(item) for item in files]
    prefix = utila.forward_slash(os.path.commonpath(files))

    # remove first slash
    files = [item.replace(prefix, '')[1:] for item in files]
    files = [item.replace('.pdf', '') for item in files]
    files = [item.replace('/', '_') for item in files]

    return files
