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
import elements.headline
import utila


def decide_headlines(clusters, cluster_size_min: int = 5):
    # find headline cluster
    flat, delete = valid_headline_clusters(clusters, cluster_size_min)
    h1_size, h2_size, h3_size, h4_size = group_headline_size(
        flat,
        cluster_size_min=cluster_size_min,
    )
    hx_font = (
        select_font(h1_size, flat),
        select_font(h2_size, flat),
        select_font(h3_size, flat),
        select_font(h4_size, flat),
    )
    hx_before = (
        select_before(h1_size, flat),
        select_before(h2_size, flat),
        select_before(h3_size, flat),
        select_before(h4_size, flat),
    )
    hx_after = (
        select_after(h1_size, flat),
        select_after(h2_size, flat),
        select_after(h3_size, flat),
        select_after(h4_size, flat),
    )
    result = (
        (h1_size, h2_size, h3_size, h4_size),
        hx_font,
        hx_before,
        hx_after,
        delete,
    )
    return result


def group_headline_size(
    items,
    cluster_size_min: int = 5,
    fontsize_diff_max: float = 0.25,
):
    sizes = sorted([item[0].style.textsize() for item in items])
    grouped = [
        statistics.mean(group)
        for group in utila.groupby_diff(sizes, maxdiff=fontsize_diff_max)
        if len(group) >= cluster_size_min
    ]
    grouped = utila.roundme(grouped, convert=False)
    grouped = sorted(grouped, reverse=True)
    h1_size, h2_size, h3_size, h4_size = None, None, None, None
    with contextlib.suppress(IndexError):
        h1_size = grouped[0]
        h2_size = grouped[1]
        h3_size = grouped[2]
        h4_size = grouped[3]
    return h1_size, h2_size, h3_size, h4_size


def valid_headline_clusters(
    clusters,
    cluster_size_min: int = 5,
    cluster_rate_min: float = 0.3,
    cluster_headline_median_length_min: int = 10,
    x0_max_diff: float = 100.0,
    whitespace_rate_max: float = 0.2,
):
    collected = []
    delete = []
    for cluster in clusters:
        cluster = clean_cluster(cluster, x0_max_diff=x0_max_diff)
        if len(cluster) <= cluster_size_min:
            continue
        rate, median = headline_rate(cluster)
        if rate < cluster_rate_min:
            continue
        if median < cluster_headline_median_length_min:
            continue
        if noheadline_cluster(cluster):
            continue
        if whitespace_rate(cluster) > whitespace_rate_max:
            continue
        collected.append(cluster)
        delete.append(cluster)
    flat = utila.flatten(collected)
    return flat, delete


def clean_cluster(
    cluster,
    x0_max_diff: float = 15.0,
    ymin: float = 0.0,
    ymax: float = 841.89 - 120,
):
    # TODO: ACCEPT RIGHT PADDED TEXT
    # skip too right items
    valid = [
        item for item in cluster
        if 35.0 <= item[0].bounding.x0 < (75.0 + x0_max_diff)
    ]
    # skip `Kapitel 1`-pattern
    valid = [
        item for item in valid
        if not elements.headline.noheadline_pattern(item[0].text)
    ]
    # TODO: THIS REMOVES ALL HEADLINES WITH NUMBER AT THE END
    # remove:
    # 5.1. ZUSAMMENFASSUNG DER ERGEBNISSE UND SCHLUSSFOLGERUNGEN   198
    # 5.2. KÜNFTIGE HERAUSFORDERUNGEN       203
    valid = [
        item for item in valid
        if not utila.isnumber(item[0].text.split(' ')[-1])
    ]
    valid = [
        item for item in valid
        if ymin <= item[0].bounding.y0 <= item[0].bounding.y1 <= ymax
    ]
    return valid


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


def select_before(size, headlines):
    if size is None:
        return None
    selected = [
        item for item in headlines
        if utila.near(size, item[0].bounding_mean, diff=0.5)
    ]
    befores = [
        current.bounding.y1 - before.bounding.y1
        for current, before, _ in selected
        if current != before
    ]
    if not befores:
        return None
    befores = utila.roundme(befores, digits=0, convert=False)
    result = utila.mode(befores, minimize=False)
    return result


def select_after(size, headlines):
    if size is None:
        return None
    selected = [
        item for item in headlines
        if utila.near(size, item[0].bounding_mean, diff=0.5)
    ]
    afters = [
        after.bounding.y1 - current.bounding.y1
        for current, _, after in selected
        if current != after
    ]
    if not afters:
        return None
    afters = utila.roundme(afters, digits=0)
    result = utila.mode(afters, minimize=False)
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


def whitespace_rate(cluster) -> float:
    charcount = 0
    whitespaces = 0
    for item in cluster:
        charcount += len(item[0].text)
        whitespaces += item[0].text.count(' ')
    if not charcount:
        return 0.0
    return whitespaces / charcount


def noheadline_cluster(cluster, pagerate_max: float = 0.5):
    """\
     2. Klassifikation 5
     3. Steuerung 13
     4. Anwendung 17
    """
    if len(cluster) < 4:
        return False
    with_pageending = [
        item for item in cluster if utila.isnumber(item[0].text.split(' ')[-1])
    ]
    pagerate = len(with_pageending) / len(cluster)
    if pagerate > pagerate_max:
        return True
    return False
