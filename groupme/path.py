# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def area(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'groupme', 'area_area', prefix)


def border_leftright(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'groupme',
        'border_leftright',
        prefix,
    )


def distance(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'groupme', 'distance_distance', prefix)


def pagenumbers(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'groupme',
        'pagenumbers_pagenumbers',
        prefix,
    )


def headerfooters(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'groupme',
        'footer_footerheader',
        prefix,
    )


def toc(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'groupme', 'toc_toc', prefix)


def figuretable(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'groupme',
        'figuretable_figuretable',
        prefix,
    )


def tabletable(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'groupme',
        'tabletable_tabletable',
        prefix,
    )
