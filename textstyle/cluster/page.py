# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum
import typing

import hey.classificator
import textstyle


class ClusterProperty(enum.Enum):
    SIZE = enum.auto()
    FONT = enum.auto()
    BEFORE = enum.auto()
    AFTER = enum.auto()
    YPOS = enum.auto()


ClusterPropertySelection = typing.List[ClusterProperty]


def flatten(pages: textstyle.PageTextPropertiesList) -> textstyle.TextProperties: # yapf:disable
    result = []
    for page in pages:
        for length, size, font, after in zip(
                page.length,
                page.sizes,
                page.fonts,
                page.distances,
        ):
            result.append(
                textstyle.TextProperty(
                    length=length,
                    size=size,
                    font=font,
                    before=None,
                    after=after,
                    ypos=None,
                ))
    return result


def cluster(items, selection: ClusterPropertySelection = None):
    if selection:
        selection = set(selection)

    def classifier(candidat, clusteritem):
        if selection is None or ClusterProperty.SIZE in selection:
            if candidat.size != clusteritem.size:
                return False
        if selection is None or ClusterProperty.AFTER in selection:
            if candidat.after != clusteritem.after:
                return False
        return True

    clustered = hey.classificator.determine_cluster(
        items,
        classifier=classifier,
    )
    return clustered
