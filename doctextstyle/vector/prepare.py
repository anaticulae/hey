# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import itertools
import os
import warnings

import iamraw
import numpy as np
import scipy.cluster.vq
import serializeraw
import texmex
import utilo

import doctextstyle.parser
import doctextstyle.utils
import magic.path

NUMPY_SEED = 1 * 2 * 4 * 8 * 16 * 32 * 64


def create_matrix(
    source: str,
    pages: tuple = None,
) -> tuple[np.array, texmex.PTNs, iamraw.FontStore]:
    loaded = serializeraw.ptn_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    magics = magic.path.content_oneline(source)
    if os.path.exists(magics):
        magics = serializeraw.load_magic_types(magics, pages=pages)
    else:
        magics = []
    fontstore = serializeraw.fs_frompath(source, pages=pages)
    matrix, loaded, fontstore = create_matrix_fromdata(
        loaded,
        fontstore,
        magics,
    )
    return matrix, loaded, fontstore


def create_matrix_fromdata(
    loaded: texmex.PTNs,
    fontstore: iamraw.FontStore,
    magics: iamraw.PageContentContentTypes = None,
) -> tuple[np.array, texmex.PTNs, iamraw.FontStore]:
    parsed = doctextstyle.parser.parses(
        loaded,
        parser=doctextstyle.parser.parse_vector,
        magics=magics,
        fontstore=fontstore,
    )
    merged = doctextstyle.utils.connect_pages(parsed)
    # TODO: UUSE NUMPY
    merged = list(itertools.zip_longest(*merged))
    # round it
    merged: np.array = np.array(merged, dtype=np.uint32)
    matrix = np.array(merged, dtype=np.double)
    return matrix, loaded, fontstore


def clusterme(matrix, navis, numbers: int = 20, runtime: int = 12000):
    # running kmeans with invalid `k`/`numbers` leads to non determining loop.
    assert isinstance(numbers, int), type(numbers)
    merged = scipy.cluster.vq.whiten(matrix)
    if len(merged) < numbers:
        utilo.error(f'too few data: {len(merged)} to run vector strategy')
        return []
    # TODO: REMOVE AFTER HAVING A MORE STABLE ALGO
    np.random.seed(NUMPY_SEED)
    _, label = scipy.cluster.vq.kmeans2(
        merged,
        k=numbers,
        iter=runtime,
        minit='points',
    )
    data = np.array(merge_neighbors(navis))
    assert len(data) == len(label), f'{len(data)} == {len(label)}'
    grouped = [data[label == item] for item in range(numbers)]
    # remove empty cluster
    notempty = [item for item in grouped if len(item)]
    return notempty


def merge_neighbors(navis):
    result = []
    for page in navis:
        if not page:
            continue
        befores = [page[0]] + page[:-1]
        afters = page[1:] + [page[-1]]
        content = list(zip(page, befores, afters))
        result.extend(content)
    return result


def disable_warnings():
    # TODO: DO NOT DISABLE ALL WARNINGS
    nowarning = lambda message, category=None, stacklevel=1, source=None: ''  # pylint:disable=W0613
    warnings.warn = nowarning


disable_warnings()
