# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import itertools
import warnings

import numpy as np
import scipy.cluster.vq
import serializeraw
import utila

import doctextstyle.parser
import doctextstyle.utils

NUMPY_SEED = 1 * 2 * 4 * 8 * 16 * 32 * 64


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
    matrix = np.array(merged, dtype=np.double)
    return matrix, loaded, fontstore


def clusterme(matrix, navis, numbers: int = 20, runtime: int = 12000):
    # running kmeans with invalid `k`/`numbers` leads to non determining loop.
    assert isinstance(numbers, int), type(numbers)
    merged = scipy.cluster.vq.whiten(matrix)
    # TODO: REMOVE AFTER HAVING A MORE STABLE ALGO
    np.random.seed(NUMPY_SEED)
    _, label = scipy.cluster.vq.kmeans2(
        merged,
        k=numbers,
        iter=runtime,
        minit='points',
    )
    data = np.array([item for item in utila.flatten(navis)])
    assert len(data) == len(label)
    grouped = [data[label == item] for item in range(numbers)]
    return grouped


def disable_warnings():
    # TODO: DO NOT DISABLE ALL WARNINGS
    nowarning = lambda message, category=None, stacklevel=1, source=None: ''  # pylint:disable=W0613
    warnings.warn = nowarning


disable_warnings()
