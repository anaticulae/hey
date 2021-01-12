# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utilatest

import magic
import magic.cli

run = functools.partial(  #pylint: disable=invalid-name
    utilatest.run_command,
    main=magic.cli.main,
    process=magic.PROCESS,
    success=True,
)
fail = functools.partial(  #pylint: disable=invalid-name
    utilatest.run_command,
    main=magic.cli.main,
    process=magic.PROCESS,
    success=False,
)
