# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import concurrent.futures
import os
import os.path

import utila

import detector.feature.titlepage as dft


def extract(files: list, destination: str, pages='0:10', worker=5):
    if os.path.exists(destination):
        return

    for pdf in files:
        assert pdf.endswith('.pdf') and os.path.exists(pdf), str(pdf)

    # ensure that generation directory exists
    os.makedirs(destination)

    def run_job(job: str):
        completed = utila.run(job)
        utila.assert_success(completed)

    generated = generate(files, destination, pages=pages)

    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = {executor.submit(run_job, pdf): pdf for pdf in generated}
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception:
                utila.info(f'{future} failed.')
                raise


def generate(files: list, outpath: str, pages: str) -> list:
    todo = []
    names = output_names(files)
    for inpath, output in zip(files, names):
        next_job = create_job(
            inpath,
            os.path.join(outpath, output),
            pages=pages,
        )
        todo.append(next_job)
    return todo


def create_job(src: str, dest: str, pages: tuple = None) -> str:
    """Create job to run required steps for next processing unit.

    Args:
        src: pdf file for processing
        dest: output path to output folder
        pages: shrink processing if given - if None process all pages
    Returns:
        Created process todo description.
    """
    assert os.path.exists(src), str(src)

    oneline = dft.RAWMAKER_CONFIGURATION
    # TODO: USE A MORE GENERAL PLACE
    config = '--all --char_margin=5.0 --boxes_flow=1.0 --line_margin=0.3'

    pages = f'--pages={pages}' if pages is not None else ''
    task = [
        f'rawmaker -j 8 -i {src} -o {dest} {config} {pages}',
        f'rawmaker -j 8 -i {src} -o {dest} {oneline} {pages}',
        f'groupme -i {dest} -o {dest}',
        f'sections -i {dest} -o {dest}',
        f'words -i {dest} -o {dest}',
    ]
    todo = ' && '.join(task)
    return todo


def output_names(files):
    files = [utila.forward_slash(item) for item in files]
    prefix = utila.forward_slash(os.path.commonpath(files))

    # remove first slash
    files = [item.replace(prefix, '')[1:] for item in files]
    files = [item.replace('.pdf', '') for item in files]
    files = [item.replace('/', '_') for item in files]

    files = sorted(files)
    return files
