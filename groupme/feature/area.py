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
import texmex
import utila
import yaml

import groupme.utils

RECTANGLE_MAX_DIFF = 10.0  # TODO: HOLY VALUE

RequiredResources = collections.namedtuple(
    'RequiredResources',
    'textnavigator, tables, boxes',
)

PageContentTextualArea = collections.namedtuple(
    'PageContentTextualArea',
    'page, textual, outside, border',
)
PageContentTextualAreas = typing.List[PageContentTextualArea]


def work(
        boxes: str,
        tables: str,
        text: str,
        textpositions: str,
        pages: tuple = None,
) -> str:
    """Extract different areas out of given data.

    Args:
        boxes(str): path to extract `rawmaker` content boxes
        tables(str): path to extracted `linero` tables
        text(str): extracted `rawmaker` text
        textpositions(str): positions of extracted text
        pages(tuple): tuple of pages to process
    Returns:
        Dumped extracted areas.
    """
    loaded = load(
        boxes=boxes,
        pages=pages,
        tables=tables,
        text=text,
        textpositions=textpositions,
    )

    grouped = group_areas(loaded=loaded)

    dumped = dump_area(grouped)
    return dumped


def group_areas(loaded: RequiredResources) -> PageContentTextualAreas:
    result = []
    for navigator in loaded.textnavigator:
        page = navigator.page

        tables = utila.select_page(loaded.tables, page)

        boxes = utila.select_page(loaded.boxes, page)
        boxes = boxes.content if boxes else None

        grouped = group_page(navigator, tables=tables, boxes=boxes)
        result.append(grouped)
    return result


def group_page(navigator, tables, boxes) -> PageContentTextualArea:
    if tables:
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
    textual = utila.rectangle_merge(textual)
    inside_tables = utila.rectangle_merge(inside_tables)
    inside_boxes = utila.rectangle_merge(inside_boxes)
    outside = {
        'boxes': inside_boxes,
        'tables': inside_tables,
    }
    border = {
        key: [item for item in value] for key, value in [
            ('boxes', boxes.content if boxes else []),
            ('tables', tables.content if tables else []),
        ]
    }
    result = PageContentTextualArea(
        page=navigator.page,
        textual=textual,
        outside=outside,
        border=border,
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


def load(
        boxes: str,
        tables: str,
        text: str,
        textpositions: str,
        pages: tuple = None,
) -> RequiredResources:
    text = serializeraw.load_document(text, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)
    textnavigator = texmex.create_pagetextnavigators(
        text,
        text_positions=textpositions,
    )
    boxes = serializeraw.load_boxes(boxes, pages=pages)
    tables = serializeraw.load_tables(tables, pages=pages)
    result = RequiredResources(
        boxes=boxes,
        tables=tables,
        textnavigator=textnavigator,
    )
    return result


def dump_area(items) -> str:
    raw = []
    for page in items:
        outside = {
            key: [tuple_tostr(item) for item in value
                 ] if value else value for key, value in page.outside.items()
        }
        border = {
            key: [tuple_tostr(item) for item in border
                 ] if border else border for key, border in page.border.items()
        }
        textual = page.textual
        if textual:
            textual = [tuple_tostr(item) for item in textual]

        content = {
            'border': border,
            'outside': outside,
            'page': page.page,
            'textual': textual,
        }
        raw.append(content)
    dumped = yaml.dump(raw)
    return dumped


def load_area(content: str, pages: tuple = None) -> PageContentTextualAreas:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(content)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        if utila.should_skip(pagenumber, pages):
            continue
        textual = [utila.parse_tuple(item) for item in page['textual']
                  ] if page['textual'] else page['textual']
        outside = {
            key:
            [utila.parse_tuple(item) for item in values] if values else values
            for key, values in page['outside'].items()
        }
        border = {
            key:
            [utila.parse_tuple(item) for item in values] if values else values
            for key, values in page['border'].items()
        }
        result.append(
            PageContentTextualArea(
                border=border,
                outside=outside,
                page=pagenumber,
                textual=textual,
            ))
    return result


def tuple_tostr(item):
    item = utila.roundme(item)
    item = [str(var) for var in item]
    return ' '.join(item)
