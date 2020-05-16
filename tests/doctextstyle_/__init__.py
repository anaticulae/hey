# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila

import doctextstyle
import doctextstyle.cli

run = functools.partial(  #pylint: disable=invalid-name
    utila.run_command,
    main=doctextstyle.cli.main,
    process=doctextstyle.PROCESS,
    success=True,
)
fail = functools.partial(  #pylint: disable=invalid-name
    utila.run_command,
    main=doctextstyle.cli.main,
    process=doctextstyle.PROCESS,
    success=False,
)
