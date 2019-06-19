# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
    Required resources:
        * text
        * font
        * position
        * page-size, to determine the distance from left border to text
"""
from functools import partial

from utila import run_command

from words import PROCESS_NAME
from words.command import main

#pylint:disable=C0103
run_words_success = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

run_words_failure = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)
