# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from functools import partial

from utila import run_command

from detector import PROCESS_NAME
from detector.cli import main

#pylint:disable=C0103
run_detector_success = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

run_detector_failure = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)
