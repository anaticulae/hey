#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from functools import partial

from iamraw import BoundingBox
from pytest import fixture
from utila import run_command

from groupme.command import PROCESS_NAME
from groupme.command import main
from groupme.textnavigator.navigator import PageTextNavigator

#pylint: disable=invalid-name
run_success = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

run_failure = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)

SAMPLE = [
    (0, BoundingBox.from_str("130.91 668.55 540.00 704.02")),
    (2, BoundingBox.from_str("358.45 605.24 480.47 625.77")),
    (1, BoundingBox.from_str("467.46 650.40 540.00 667.51")),
    (4, BoundingBox.from_str("409.67 513.88 540.01 558.02")),
    (5, BoundingBox.from_str("550.0 513.88 600.0 558.02")),
    (3, BoundingBox.from_str("304.91 587.31 534.01 607.84")),
    (6, BoundingBox.from_str("77.38 216.25 121.22 230.47")),
    (8, BoundingBox.from_str("303.26 40.18 308.74 54.44")),
    (7, BoundingBox.from_str("77.38 102.67 534.62 206.45")),
]


@fixture
def navigator() -> PageTextNavigator:
    result = PageTextNavigator()
    for item, position in SAMPLE:
        result.insert(position, item)
    assert len(result) == len(SAMPLE)
    return result
