# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila

from detector import PROCESS_NAME
from detector.cli import main

#pylint:disable=C0103
run_detector_success = functools.partial(
    utila.run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

run_detector_failure = functools.partial(
    utila.run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)
