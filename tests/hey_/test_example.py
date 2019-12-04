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

import hey.example
import tests.resources


def test_hey_example_common_root():
    pdfs = [
        tests.resources.PYPORTING_PDF,
        tests.resources.BACHELOR_111PAGES_PDF,
    ]
    expected = [
        'bachelor_page_111_images_toc',
        'docu_porting_extension_modules',
    ]

    root = hey.example.output_names(pdfs)

    assert root == expected


@utila.skip_longrun
def test_hey_example_extract(testdir):
    root = str(testdir)
    generated = os.path.join(root, 'generated')
    pdfs = [
        tests.resources.PYPORTING_PDF,
        tests.resources.BACHELOR_111PAGES_PDF,
    ]
    hey.example.extract(pdfs, generated)

    assert os.path.exists(generated), str(generated)
