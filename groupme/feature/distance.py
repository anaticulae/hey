# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Distance detector
=================

Compute the distance between textual and non textual elements.

There are two differences for every non textual elements. The distance
before(negative) and the distance after(positive). If the page starts or
ends with an non textual element, the distance is None.

TODO: SUPPORT LEFT RIGHT DISTANCE

"""

import collections
import typing

import serializeraw
import texmex
import utila
import yaml

import groupme.feature.area

RequiredResources = collections.namedtuple(
    'RequiredResources',
    'area, textnavigator',
)

AreaDistance = collections.namedtuple(
    'AreaDistance',
    'index, before, after',
)
AreaDistances = typing.List[AreaDistance]

PageContentAreaDistance = collections.namedtuple(
    'PageContentAreaDistance',
    'page, content',
)
PageContentAreaDistances = typing.List[PageContentAreaDistance]


def work(
        area: str,
        text: str,
        textpositions: str,
        pages: tuple = None,
) -> str:
    loaded = load(area, text, textpositions, pages=pages)

    distances = determine_distances(loaded)

    dumped = dump_distance(distances)
    return dumped


def determine_distances(loaded: RequiredResources) -> PageContentAreaDistances:
    result = []
    for navigator in loaded.textnavigator:
        page = navigator.page
        areas = utila.select_page(loaded.area, page)
        grouped = group_page(navigator, areas)
        if not grouped:
            continue
        result.append(PageContentAreaDistance(content=grouped, page=page))
    return result


def group_page(navigator, areas) -> AreaDistances:
    distance = create_distance(areas.border)
    distances = [distance.distance(line.bounding) for line in navigator]

    collected = collections.defaultdict(list)
    for item in distances:
        if not item:
            continue
        values, index = item
        if isinstance(values, float):
            collected[index].append(values)
        else:
            collected[index].append(values[0])
            collected[index + 1].append(values[1])

    final = []
    for key, value in collected.items():
        negative = max([item for item in value if item < 0], default=None)
        positive = min([item for item in value if item >= 0], default=None)

        negative = utila.roundme(negative) if negative is not None else None
        positive = utila.roundme(positive) if positive is not None else None
        final.append(AreaDistance(index=key, before=negative, after=positive))
    return final


class Distance:

    def __init__(self, diff: float = 10.0):
        self.content = []
        self.sorted = True
        self.diff = diff

    def distance(self, bounding):  # pylint:disable=R1260,R0911
        if not self:
            return None
        if not self.sorted:
            self.sort()
        top, bottom = bounding[1], bounding[3]
        if len(self) == 1:
            if utila.rectangle_inside(self[0], bounding, diff=self.diff):
                return None
            top_current = self[0][1]
            bottom_current = self[0][3]
            if bottom <= top_current:
                # content is above
                return (utila.roundme(bottom - top_current), 0)
            # content is below
            return (utila.roundme(top - bottom_current), 0)

        if self[-1][3] <= bounding[1]:
            # after
            return (utila.roundme(bounding[1] - self[-1][3]), len(self) - 1)

        # in the middle
        for index, (before, after) in enumerate(zip(self[0:-1], self[1:])):
            bottom_before = before[3]
            top_after = after[1]
            if utila.rectangle_inside(before, bounding):
                return None
            if utila.rectangle_inside(after, bounding):
                return None
            if bottom_before <= top <= bottom <= top_after:
                diff_top = top - bottom_before
                diff_bottom = bottom - top_after
                return (diff_top, diff_bottom), index
        return None

    def append(self, item):
        self.content.append(item)
        self.sorted = False

    def sort(self):
        self.content = sorted(self.content, key=lambda item: item[1])
        self.sorted = True

    def __getitem__(self, index):
        return self.content[index]

    def __len__(self):
        return len(self.content)


def create_distance(items) -> Distance:
    result = Distance()
    for values in items.values():
        for item in values:
            result.append(item)
    result.sort()
    return result


def load(
        area: str,
        text: str,
        textpositions: str,
        pages: tuple = None,
) -> RequiredResources:
    area = groupme.feature.area.load_area(area, pages=pages)
    text = serializeraw.load_document(text, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)
    textnavigator = texmex.create_pagetextnavigators(
        text,
        text_positions=textpositions,
        fill_empty=False,
    )
    result = RequiredResources(
        area=area,
        textnavigator=textnavigator,
    )
    return result


def dump_distance(items: PageContentAreaDistances) -> str:
    raw = []
    for page in items:
        content = []
        for item in page.content:
            before = utila.roundme(item.before) if item.before is not None else 'None' # yapf:disable
            after = utila.roundme(item.after) if item.after is not None else 'None' # yapf:disable
            content.append(f'{item.index} {before} {after}')
        raw.append({'page': page.page, 'content': content})
    dumped = yaml.dump(raw)
    return dumped


def load_distance(
        content: str,
        pages: tuple = None,
) -> PageContentAreaDistances:
    # TODO: MOVE TO SERIALIZERAW
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(content)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        if utila.should_skip(pagenumber, pages):
            continue
        pagecontent = []
        for line in page['content']:
            index, before, after = line.split()
            try:
                before = float(before)
            except ValueError:
                before = None
            try:
                after = float(after)
            except ValueError:
                after = None
            index = int(index)
            pagecontent.append(
                AreaDistance(
                    index=index,
                    before=before,
                    after=after,
                ))
        result.append(
            PageContentAreaDistance(
                page=pagenumber,
                content=pagecontent,
            ))
    return result
