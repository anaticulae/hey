# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import itertools
import typing

import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.vq
import serializeraw
import sklearn.cluster
import utila

import doctextstyle.parser
import doctextstyle.utils

Line = collections.namedtuple(
    'Line',
    'rate, upper, size, bold, italic, left, right, top, bottom',
)
Lines = typing.List[Line]


def navigators(source: str, pages: tuple = None) -> np.array:
    loaded = serializeraw.create_pagetextnavigators_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    fontstore = serializeraw.create_fontstore_frompath(source, pages=pages)
    parsed = doctextstyle.parser.parses(
        loaded,
        parser=doctextstyle.parser.parse_vector,
        fontstore=fontstore,
    )
    merged = doctextstyle.utils.connect_pages(parsed)
    # TODO: UUSE NUMPY
    merged = list(itertools.zip_longest(*merged))

    # round it
    merged = np.array(merged, dtype=np.uint32)
    result = np.array(merged, dtype=np.double)
    return result


def cluster(content, numbers: int = 20, runtime: int = 12000):
    merged = scipy.cluster.vq.whiten(content)
    centroid, label = scipy.cluster.vq.kmeans2(
        merged,
        k=numbers,
        iter=runtime,
        thresh=10.0,
    )
    counts = np.bincount(label)
    data = np.array([item.text for item in utila.flatten(loaded)])
    assert len(data) == len(label)

    grouped = [data[label == item] for item in range(numbers)]
    return grouped
