# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Headline extractor
==================

Strategies:

    - (done) Extract headlines by level
    - (todo) Extract headlines by style information

"""

import collections
import re

import elements
import texmex.style
import utila

import doctextstyle.vector.headlines


def run(source: str, pages: tuple = None):
    matrix, navis, _ = doctextstyle.vector.prepare.navigators(
        source,
        pages=pages,
    )
    clustered = doctextstyle.vector.prepare.clusterme(matrix, navis)
    result = doctextstyle.vector.extract.extract_headlines(clustered)
    return result


def extract_headlines(clusters, cluster_size_min: int = 5):
    # find headline cluster
    flat, _ = doctextstyle.vector.headlines.valid_headline_clusters(
        clusters,
        cluster_size_min,
    )
    # merge multiple headline
    flat = merge_headline(flat)
    # sort headlines
    flat = sorted(flat, key=lambda x: utila.alphabetically(x.text))
    # group headlines
    grouped = groupby_level(flat)
    # verify group
    result = verify_level(grouped)
    return result


def groupby_level(items):
    # TODO: ADD HEADLINE SIZE GROUPING STRATEGY
    grouped = collections.defaultdict(list)
    for item in items:
        text = item.text
        level = elements.level_numbered(text)
        if level is False:
            level = 4
        if level is None:
            level = 4
        grouped[level - 1].append(item)
    result = [grouped[number] for number in range(len(grouped))]
    return result


def merge_headline(items):
    """Merge multi-line-headlines into a single line."""
    result = []
    done = set()
    for current, before, after in items:
        # use id to use object and not hashed object, cause it is possible
        # than two items of different pages are complete identically.
        if id(current) in done:
            # use item only onces
            continue
        if current.style.fontid != after.style.fontid:
            result.append(current)
            done.add(id(current))
            continue
        if current.style.fontid == before.style.fontid:
            if current == before:
                # start of page
                bounding = utila.rectangle_max((
                    current.bounding,
                    after.bounding,
                ))
                new = texmex.style.TextInfo(
                    text=f'{current.text.strip()} {after.text.strip()}',
                    style=current.style,
                    bounding=bounding,
                    bounding_mean=current.bounding_mean,
                )
                result.append(new)
                done.add(id(current))
                done.add(id(after))
            else:
                # all styles are equal, merge three of them
                bounding = utila.rectangle_max((
                    before.bounding,
                    current.bounding,
                    after.bounding,
                ))
                new = texmex.style.TextInfo(
                    text=
                    f'{before.text.strip()} {current.text.strip()} {after.text.strip()}',
                    style=current.style,
                    bounding=bounding,
                    bounding_mean=current.bounding_mean,
                )
                result.append(new)
                done.add(id(current))
                done.add(id(before))
                done.add(id(after))
    return result


CHAPTER_PATTERN = re.compile(r'^(Kapitel|Chapter)[ ]{0,5}\d', re.IGNORECASE)


def verify_level(grouped: list) -> list:
    result = []
    for group in grouped:
        if not any([CHAPTER_PATTERN.match(item.text) for item in group]):
            result.append(group)
            continue
        # remove no-chapter-pattern
        valid = [item for item in group if CHAPTER_PATTERN.match(item.text)]
        result.append(valid)
        # TODO: MOVE INVALID TO GROUP LEVEL 4?
    return result
