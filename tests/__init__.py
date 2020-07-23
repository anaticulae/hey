# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import hey
import tests.resources

power.setup(hey.ROOT)


def relative_path(item):
    item = item.replace(power.REPOSITORY, '')
    start_with_slash = item[0] in ('/', '\\')
    if start_with_slash:
        item = item[1:]

    item = utila.forward_slash(item)
    return item


def prepare(item):
    return item.replace(utila.NEWLINE, '').replace(' ', '_')[0:40]
