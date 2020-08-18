# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utilatest

import hey.example


def test_hey_example_common_root():
    pdfs = [
        power.DOCU09_PDF,
        power.BACHELOR111_PDF,
    ]
    expected = {
        'bachelor_page_111_images_toc',
        'docu_porting_extension_modules',
    }

    root = utilatest.simplify_testfile_names(pdfs)
    # the expected order is not important
    root = set(root)  # pylint:disable=R0204

    assert root == expected


@utilatest.skip_nightly
def test_hey_example_extract(testdir):
    root = str(testdir)
    generated = os.path.join(root, 'generated')
    pdfs = [
        power.DOCU09_PDF,
        power.BACHELOR111_PDF,
    ]
    hey.example.extract(
        pdfs,
        generated,
        pages='0:5',
        groupme=True,
        doctextstyle=True,
    )
    assert os.path.exists(generated), str(generated)
