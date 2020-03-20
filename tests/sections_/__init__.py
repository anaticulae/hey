# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from functools import partial

from iamraw import Document
from pytest import fixture
from serializeraw import load_document
from serializeraw import load_horizontals
from utila import run_command

from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from sections import PROCESS
from sections.cli import main

#pylint:disable=C0103
run_sections = partial(
    run_command,
    main=main,
    process=PROCESS,
    success=True,
)

run_sections_failure = partial(
    run_command,
    main=main,
    process=PROCESS,
    success=False,
)
