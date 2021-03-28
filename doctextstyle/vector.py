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
import statistics
import typing
import warnings

import elements
import iamraw
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


def clusterme(matrix, navis, numbers: int = 20, runtime: int = 12000):
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


def decide(clustered, fontstore) -> iamraw.DocTextStyle:
    notempty = [item for item in clustered if len(item)]
    text_ = largest(notempty)
    notempty = notempty[0:text_] + notempty[text_:]
    text = notempty[text_]
    text_size, text_distance, text_family = decide_text(text)
    headlines, deletes = decide_headlines(notempty)
    deletes = {hash(str(item)) for item in deletes}
    notempty = [item for item in notempty if hash(str(item)) not in deletes]

    result = iamraw.DocTextStyle(
        text_size=text_size,
        text_distance=text_distance,
        text_family=fontstore[text_family].name,
        h1_size=headlines[0],
        h2_size=headlines[1],
        h3_size=headlines[2],
        h4_size=headlines[2],
    )
    return result


def decide_text(text):
    first = text[0].style
    return first.textsize(), -1, first.fontid


def decide_headlines(clusters, cluster_min_size: int = 5):
    # find headline cluster
    collected = []
    delete = []
    for cluster in clusters:
        rate, median = headline_rate(cluster)
        if rate < 0.30 or median < 10:
            continue
        if noheadline_cluster(cluster):
            continue
        # TODO: ACCEPT RIGHT PADDED TEXT
        # skip too right items
        valid = [
            item for item in cluster if utila.near(
                75.0,
                item.bounding.x0,
                diff=10.0,  # TODO: HOLY VALUE
            )
        ]
        if len(valid) <= cluster_min_size:
            continue
        collected.append(valid)
        delete.append(cluster)
    flat = utila.flatten(collected)
    sizes = sorted([item.bounding_mean for item in flat], reverse=True)
    grouped = [
        statistics.mean(group)
        for group in utila.groupby_diff(sizes)
        if len(group) >= cluster_min_size
    ]
    h1_size, h2_size, h3_size, h4_size = None, None, None, None
    return (
        h1_size,
        h2_size,
        h3_size,
        h4_size,
    ), delete


def headline_rate(cluster):
    # TODO: MOVE TO ELEMENTS?
    median = statistics.median([len(item.text) for item in cluster])
    headlines = [
        item for item in cluster if elements.isheadline(
            item.text,
            strict=False,
        )
    ]
    return len(headlines) / len(cluster), median


def noheadline_cluster(cluster, pagerate_max: float = 0.5):
    """\
     2. Klassifikation 5
     3. Steuerung 13
     4. Anwendung 17
    """
    if len(cluster) < 4:
        return False
    with_pageending = [
        item for item in cluster if utila.isnumber(item.text.split(' ')[-1])
    ]
    pagerate = len(with_pageending) / len(cluster)
    if pagerate > pagerate_max:
        return True
    return False


def largest(items) -> int:
    if not items:
        raise ValueError('empty collection')
    longest = 0
    for index, item in enumerate(items[1:], start=1):
        if len(item) < len(items[longest]):
            continue
        longest = index
    return longest


def disable_warnings():
    # TODO: DO NOT DISABLE ALL WARNINGS
    nowarning = lambda message, category=None, stacklevel=1, source=None: ''  # pylint:disable=W0613
    warnings.warn = nowarning


disable_warnings()
