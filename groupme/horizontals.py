# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import utila

import groupme
import groupme.likelihood


def match(
        content: iamraw.PageContentHorizontals,
        vertical_position: float,
) -> bool:
    """Check if any horizontal match the `vertical_position`

    Args:
        content(PageContentHorizontals): list with horizontal lines,
                                         mostly one page
        vertical_position(float): position on the page in 'pixel'
    Returns:
        True if any horizontal line match the `vertical_position`
    """
    vertical = utila.roundme(vertical_position)
    # TODO: Check y0/y1
    return any([utila.roundme(item.box.y0) == vertical for item in content])


def assert_horizontal(bounding):
    # TODO HOLY VALUE
    # assert abs(bounding.y0 - bounding.y1) < 2.0, str(bounding)
    # assert that item is horizontal
    assert abs(bounding.y0 - bounding.y1) < 2.0, str(bounding)


def biggest_hlinecluster_in_area(
        clusters: typing.List,
        ymin: float,
        ymax: float,
        max_group_count: int = 1,  # pylint:disable=W0613
        min_group_size: int = 1,
) -> typing.List[int]:
    """Determine cluster with maximal horizontal line count which fits
    in area between [ymin and ymax]. Return y-coordinate of cluster as a
    footer/header-border.

    Args:
        clusters: list of horizontal line cluster
        ymin: top y-bound of valid area
        ymax: bottom y-bound of valid area
        max_group_count: number of groups to detect(not supported yet)
        min_group_size: minimal amout of member in valid cluster
    Returns:
        `y-coordinate` of most matching cluster
        `None` if no cluster match [ymin,ymax] area
    """
    assert len(clusters) >= 1, 'no clusters provided'
    valid = cluster_in_area(clusters, ymin, ymax)
    if not any([item for item in valid]):
        # no cluster is in range
        return None

    # remove clusters with to few elements
    valid = [item for item in valid if len(item) >= min_group_size]

    maximized = groupme.likelihood.select_maxi(valid, count=max_group_count)
    result = []
    for cluster in maximized:
        first_cluster_item = cluster[0]
        _, (bounding, __) = first_cluster_item  # select first item of cluster
        result.append(bounding.y1)
    return result


def cluster_in_area(clusters, ymin, ymax):
    """How many horizontals lines of `cluster` are in range of [ymin,
    ymax].

    Iterate through `clusters` and check if `cluster` is in area of ymin
    to ymax.

    Args:
        clusters(list):
        ymin(int): top bounds
        ymax: bottom bounds
    """
    result = []
    for cluster in clusters:
        # take first item in cluster to determine cluster location,
        # because all items in cluster have the same location.
        _, (bounding, __) = cluster[0]
        groupme.horizontals.assert_horizontal(bounding)

        if groupme.utils.between(bounding, ymin, ymax):
            result.append(cluster)
    return result
