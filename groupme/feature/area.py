# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Textual Area
============

TODO:
 * table of content
 * images
 * reference table

"""

import collections
import typing

import serializeraw
import utila
import yaml

import groupme.utils
import hey.textnavigator.navigator

RequiredResources = collections.namedtuple(
    'RequiredResources',
    'textnavigator, tables, boxes',
)

PageContentTextualArea = collections.namedtuple(
    'PageContentTextualArea',
    'page, textual, outside',
)
PageContentTextualAreas = typing.List[PageContentTextualArea]


def work(
        text: str,
        textpositions: str,
        tables: str,
        boxes: str,
        pages: tuple = None,
) -> str:
    loaded = load(
        text=text,
        textpositions=textpositions,
        tables=tables,
        boxes=boxes,
        pages=pages,
    )

    grouped = group_areas(loaded=loaded)

    dumped = dump_area(grouped)
    return dumped


def load(
        text: str,
        textpositions: str,
        tables: str,
        boxes: str,
        pages: tuple = None,
) -> RequiredResources:
    text = serializeraw.load_document(text, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)
    textnavigator = hey.textnavigator.navigator.create_pagetextnavigators(
        text,
        text_positions=textpositions,
    )
    boxes = serializeraw.load_boxes(boxes, pages=pages)
    tables = serializeraw.load_tables(tables, pages=pages)
    result = RequiredResources(
        textnavigator=textnavigator,
        tables=tables,
        boxes=boxes,
    )
    return result


def group_areas(loaded: RequiredResources):
    result = []
    for navigator in loaded.textnavigator:
        page = navigator.page

        tables = utila.select_page(loaded.tables, page)

        boxes = utila.select_page(loaded.boxes, page)
        boxes = boxes.content if boxes else None

        grouped = group_page(navigator, tables=tables, boxes=boxes)
        result.append(grouped)
    return result


RECTANGLE_MAX_DIFF = 10.0  # TODO: HOLY VALUE


def group_page(navigator, tables, boxes) -> PageContentTextualArea:
    if tables:
        # tables
        tables = table_checker(tables)

    if boxes:
        boxes = boxed_checker(boxes)

    textual = []
    inside_tables = []
    inside_boxes = []
    for text in navigator:
        bounding = tuple(text.bounding)
        if tables and tables.contains(*bounding):
            inside_tables.append(bounding)
        if boxes and boxes.contains(*bounding):
            inside_boxes.append(bounding)
        else:
            textual.append(bounding)

    # optimize rectangles
    textual = groupme.utils.merge_rectangles(textual)
    inside_tables = groupme.utils.merge_rectangles(inside_tables)
    inside_boxes = groupme.utils.merge_rectangles(inside_boxes)
    outside = {
        'tables': inside_tables,
        'boxes': inside_boxes,
    }
    pagenumber = navigator.page
    result = PageContentTextualArea(
        page=pagenumber,
        textual=textual,
        outside=outside,
    )
    return result


def boxed_checker(items) -> groupme.utils.RectangleCheck:
    result = groupme.utils.RectangleCheck(max_diff=RECTANGLE_MAX_DIFF)
    for item in items:
        result.extend(*item.box)
    return result


def table_checker(items) -> groupme.utils.RectangleCheck:
    result = groupme.utils.RectangleCheck(max_diff=RECTANGLE_MAX_DIFF)
    for item in items:
        result.extend(*item.bounding)
    return result


def dump_area(items) -> str:
    raw = []
    for page in items:
        outside = {
            key: [tuple_tostr(item) for item in value
                 ] for key, value in page.outside.items()
        }
        content = {
            'page': page.page,
            'textual': [tuple_tostr(item) for item in page.textual],
            'outside': outside,
        }
        raw.append(content)
    dumped = yaml.dump(raw)
    return dumped


def load_area(content: str, pages: tuple = None) -> PageContentTextualAreas:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        if utila.should_skip(pagenumber, pages):
            continue
        textual = [utila.parse_tuple(item) for item in page['textual']]
        outside = {
            key: [utila.parse_tuple(item) for item in values
                 ] for key, values in page['outside'].items()
        }
        result.append(
            PageContentTextualArea(
                page=pagenumber,
                textual=textual,
                outside=outside,
            ))
    return result


def tuple_tostr(item):
    item = utila.roundme(item)
    item = [str(var) for var in item]
    return ' '.join(item)
