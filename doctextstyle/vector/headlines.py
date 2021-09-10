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
    flat, delete = valid_headline_clusters(
        clusters,
        cluster_size_min=cluster_size_min,
    )
    grouped = group_magic(
        flat,
        cluster_size_min=cluster_size_min,
    )
    hx_size = group_headline_size(grouped)
    hx_font = tuple(select_font(grouped[number]) for number in range(4))
    hx_before = tuple(select_before(grouped[number]) for number in range(4))
    hx_after = tuple(select_after(grouped[number]) for number in range(4))
    result = (
        hx_size,
        hx_font,
        hx_before,
        hx_after,
        delete,
    )
    return result


def group_magic(
    items,
    fontsize_diff_max: float = 0.25,
    cluster_size_min: int = 5,
) -> list:
    """Group potential headlines by font size and extracted level.

    1. Extract the level out of text content. Use None if no 1.2.3 is given
    2. Sort items by font size
    3. Group items by different level and font size
    4. Remove too little groups
    """
    # current.text,
    items = [(
        item[0].style.textsize(),
        elements.level_numbered(item[0].text),
        item,
    ) for item in items]
    # sort by level
    items.sort(key=lambda x: x[1] if x[1] is not None else 1)
    # sort by textsize
    items.sort(key=lambda x: x[0], reverse=True)
    # group data by textdiff and leveldiff
    grouped = [[items[0]]]
    for item in items[1:]:
        before = grouped[-1][0]
        fontdiff = not utila.near(
            expected=before[0],
            current=item[0],
            diff=fontsize_diff_max,
        )
        equallevel = before[1] == item[1]
        if before[1] is None and item[1] is not None:
            equallevel = False
        if before[1] is not None and item[1] is None:
            equallevel = True
        if fontdiff or not equallevel:
            # new group
            grouped.append([item])
        else:
            grouped[-1].append(item)
    result = [group for group in grouped if len(group) >= cluster_size_min]
    result = [[item[2] for item in group] for group in result]
    # fill empty groups
    while len(result) < 4:
        result.append([])
    return result


def group_headline_size(
    groups,
    strategy: callable = statistics.mean,
):
    sizes = [[item[0].style.textsize() for item in group] for group in groups]
    # determine group value
    grouped = [strategy(group) for group in sizes if group]
    # convert to user friendly result
    grouped = utila.roundme(grouped, convert=False)
    # prepare result
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


PAGE_HEIGHT = 841.89
HEADER_HEIGHT = 70.0
FOOTER_HEIGHT = 120.0


def clean_cluster(
    cluster,
    x0_max_diff: float = 15.0,
    ymin: float = HEADER_HEIGHT,
    ymax: float = PAGE_HEIGHT - FOOTER_HEIGHT,
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
    # Lebenslauf .............................. xx
    valid = [item for item in valid if item[0].text.count('.') < 6]
    # in bounds
    valid = [
        item for item in valid
        if ymin <= item[0].bounding.y0 <= item[0].bounding.y1 <= ymax
    ]
    return valid


def select_font(group):
    fonts = [item[0].style.fontid for item in group]
    if not fonts:
        # no matching font
        return None
    result = utila.maxs(fonts)
    return result


def select_before(group):
    befores = [
        current.bounding.y1 - before.bounding.y1
        for current, before, _ in group
        if current != before
    ]
    if not befores:
        return None
    befores = utila.roundme(befores, digits=0, convert=False)
    result = utila.mode(befores, minimize=False)
    return result


def select_after(group):
    afters = [
        after.bounding.y1 - current.bounding.y1
        for current, _, after in group
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
