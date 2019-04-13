#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from os.path import exists
from os.path import join

from groupme import ROOT

TEST_DATA = join(ROOT, 'tests/groupme_/data')

assert exists(TEST_DATA), TEST_DATA

SIMPLE = join(TEST_DATA, 'simple')

SIMPLE_TEXT = join(SIMPLE, 'text.yaml')
SIMPLE_TOC = join(SIMPLE, 'toc.yaml')

for item in [SIMPLE, SIMPLE_TEXT, SIMPLE_TOC]:
    msg = 'Missing resource: %s' % item
    assert exists(item), item
