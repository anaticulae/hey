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

from tests.resources import NO_TITLE_GENERATED
from tests.resources import REQURIED_RESOURCES
from tests.resources.update import extract_examples
from tests.resources.update import install_requirements
from tests.resources.update import sync_resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

# TODO: Ensure that tests waits before this process is ready

if not 'PYTEST_XDIST_WORKER' in os.environ:
    # master process only
    # ensure to avoid race condition if more than one thread tries to
    # install or use rawmaker

    if 'GENERATE' in os.environ or utila.test.LONGRUN:
        utila.log('install requirements')
        install_requirements()

        # ensure that all test resources exists
        utila.log('synchronize test resources')
        sync_resources()

        utila.log('extract resources')
        extract_examples()

CHECK = REQURIED_RESOURCES + NO_TITLE_GENERATED

for item in CHECK:
    advice = 'run `baw --test=generate` to generate test data'
    msg = f'required test path does not exists: {item}, {advice}'
    assert os.path.exists(item), msg
