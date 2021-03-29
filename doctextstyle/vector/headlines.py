# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import statistics

import elements
import utila


def decide_headlines(clusters, cluster_min_size: int = 5):
    # find headline cluster
    flat, delete = valid_headline_clusters(clusters, cluster_min_size)
    sizes = sorted([item[0].bounding_mean for item in flat])
    grouped = [
        statistics.mean(group)
        for group in utila.groupby_diff(sizes)
        if len(group) >= cluster_min_size
    ]
    grouped = utila.roundme(grouped)
    h1_size, h2_size, h3_size, h4_size = None, None, None, None
    with contextlib.suppress(IndexError):
        h1_size = grouped[-1]
        h2_size = grouped[-2]
        h3_size = grouped[-3]
        h4_size = grouped[-4]
    h1_font, h2_font, h3_font, h4_font = (
        select_font(h1_size, flat),
        select_font(h2_size, flat),
        select_font(h3_size, flat),
        select_font(h4_size, flat),
    )
    result = (
        (h1_size, h2_size, h3_size, h4_size),
        (h1_font, h2_font, h3_font, h4_font),
        delete,
    )
    return result


def valid_headline_clusters(clusters, cluster_min_size: int = 5):
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
                item[0].bounding.x0,
                diff=10.0,  # TODO: HOLY VALUE
            )
        ]
        if len(valid) <= cluster_min_size:
            continue
        collected.append(valid)
        delete.append(cluster)
    flat = utila.flatten(collected)
    return flat, delete


def select_font(size, headlines):
    if size is None:
        return None
    fonts = [
        item[0].style.fontid
        for item in headlines
        if utila.near(size, item[0].bounding_mean, diff=0.5)
    ]
    result = utila.maxs(fonts)
    return result


def headline_rate(cluster):
    # TODO: MOVE TO ELEMENTS?
    median = statistics.median([len(item[0].text) for item in cluster])
    headlines = [
        item for item in cluster if elements.isheadline(
            item[0].text,
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
        item
        for item in cluster
        if utila.isnumber(item[0].text.split(' ')[-1])
    ]
    pagerate = len(with_pageending) / len(cluster)
    if pagerate > pagerate_max:
        return True
    return False
