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

import iamraw
import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.vq
import serializeraw
import utila

import doctextstyle.parser
import doctextstyle.utils

Line = collections.namedtuple(
    'Line',
    'rate, upper, size, bold, italic, left, right, top, bottom',
)
Lines = typing.List[Line]

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


def cluster(matrix, navigators, numbers: int = 20, runtime: int = 12000):
    merged = scipy.cluster.vq.whiten(matrix)
    # TODO: REMOVE AFTER HAVING A MORE STABLE ALGO
    np.random.seed(NUMPY_SEED)
    centroid, label = scipy.cluster.vq.kmeans2(
        merged,
        k=numbers,
        iter=runtime,
        thresh=10.0,
    )
    counts = np.bincount(label)
    data = np.array([item for item in utila.flatten(navigators)])
    assert len(data) == len(label)
    grouped = [data[label == item] for item in range(numbers)]
    return grouped


def decide(clustered, fontstore) -> iamraw.DocTextStyle:
    notempty = [item for item in clustered if len(item)]
    largest_ = largest(notempty)

    text = notempty[largest_]
    text_size, text_distance, text_family = decide_text(text)

    result = iamraw.DocTextStyle(
        text_size=text_size,
        text_distance=text_distance,
        text_family=fontstore[text_family].name,
    )
    return result


def decide_text(text):
    first = text[0].style
    return first.textsize(), -1, first.fontid


def largest(items):
    if not items:
        raise ValueError('empty collection')
    longest = 0
    print([len(item) for item in items])
    for index, item in enumerate(items[1:], start=1):
        if len(item) < len(items[longest]):
            continue
        longest = index
    return longest
