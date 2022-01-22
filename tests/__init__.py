# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power

import hey

power.setup(hey.ROOT)

RESOURCES = os.path.join(hey.ROOT, 'tests/resources')
LINEDISTANCE_PDF = os.path.join(RESOURCES, 'linedistances.pdf')
assert os.path.exists(LINEDISTANCE_PDF), LINEDISTANCE_PDF

LINESGENERATED = power.generated('linedistances')

LINEDISTANCE100_PDF = os.path.join(LINESGENERATED, 'percent100.pdf')
LINEDISTANCE150_PDF = os.path.join(LINESGENERATED, 'percent150.pdf')
LINEDISTANCE200_PDF = os.path.join(LINESGENERATED, 'percent200.pdf')
