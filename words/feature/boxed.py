# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
TODO: Think about this complex data structure. Do we need this realy?
"""
from collections import defaultdict
from functools import lru_cache
from functools import partial

from iamraw import BoundingBox
from serializeraw import load_boxes
from utila import checkdatatype
from utila import error
from utila import from_raw_or_path
from utila import log
from yaml import FullLoader
from yaml import dump
from yaml import load

from hey import CACHE_SMALL
from words.boxed import NO_BOX
from words.boxed import BoxedChecker
from words.input import prepare_input
from words.input import process_input


@checkdatatype
def work(
        extracted_text: str,
        text: str,
        text_position: str,
        headlines: str,
        border: str,
        horizontals: str,
        boxes: str,
) -> str:
    """Combine `extracted_text` and check the `undefined` fields for lists

    Args:
        extracted_text(str): document with `undefined fields` from `text`
                             module of `words`
        text(str): extracted text from rawmaker
        text_position(str): position of extracted text
        headlines(str): extracted chapter/paragraph headlines of `words` module
        border(str):
    """
    extracted, _ = prepare_input(
        extracted_text,
        text,
        text_position,
        border,
        headlines,
        horizontals,
    )
    boxes = load_boxes(boxes)

    result = process_content(extracted, boxes)

    dumped = dump_boxedcontent(result)
    return dumped


def process_content(extracted, boxes: BoxedChecker):
    boxes = BoxedChecker(boxes)
    worker = partial(extract_boxed_content, boxed=boxes)
    result = process_input(extracted, worker)
    return result


def extract_boxed_content(contentblock, boxed: BoxedChecker):
    result = defaultdict(list)
    for (page, headlinenumber, headlinecontent) in contentblock:

        zipped = zip(headlinecontent[0], headlinecontent[1])
        for _, ((headlineblockid, blocks), uindexs) in enumerate(zipped):
            collected = []
            current = defaultdict(list)
            for ((bounding, line), uindex) in zip(blocks, uindexs):
                boxid = boxed.boxid(page, bounding)
                if boxid == NO_BOX:
                    # splitted by non-box-element
                    if not current:
                        continue
                    collected.append([(
                        boxed.boundingbox(page, boxid_),
                        (boxid_, uindex, content),
                    ) for boxid_, content in current.items()])
                    current = defaultdict(list)
                # add line to box, defined by `boxid`
                current[boxid].append((bounding, uindex, line))
            # item ends with box
            if current:
                collected.append([(
                    boxed.boundingbox(page, item),
                    (item, content),
                ) for item, content in current.items()])

            if collected:
                result[page].append((
                    headlinenumber,
                    headlineblockid,
                    collected,
                ))
    if not result:
        return None
    assert len(result) == 1, len(result)
    for key, value in result.items():
        return (key, value)


def dump_boxedcontent(boxed) -> str:

    # headlinenumber,
    # headlineblocknumber,
    # collected,

    # BoundingBox
    # boxid, content
    raw = []
    for (page, pagecontent) in boxed:
        pageresult = []
        for (headlinenumber, headlineblocknumber, collected) in pagecontent:
            # for (bounding, blockcontent) in collected:
            # more than one box in a box-container:
            # content, box, box, content, box, content
            single_collector = []  # crazy naming!
            for multiboxed in collected:
                items = []
                for index, item in enumerate(multiboxed):
                    try:
                        bounding, (boxid, _content) = item
                    except ValueError:
                        # TODO: INVESTIGATE WHAT HAPPENS HERE
                        error('could not convert, skip boxed: `%s`' % str(item))
                        continue
                    items.append({
                        'boxed_id':
                        '%d %d' % (boxid, index),
                        'bounding':
                        str(bounding),
                        'content': [
                            '%s %d %s' % (str(bounding), uindex, contentitem)
                            for (bounding, uindex, contentitem) in _content
                        ]
                    })
                single_collector.append(items)
            pageresult.append({
                'headlinenumber': headlinenumber,
                'headlineblocknumber': headlineblocknumber,
                'content': single_collector,
            })

        raw.append({
            'page': page,
            'content': pageresult,
        })
    dumped = dump(raw)
    return dumped


@lru_cache(CACHE_SMALL)
def load_boxedcontent(content: str):

    def _parse_box_content(line: str):
        """Returns:
            bounding(BoundingBox):
            undefined_index(int):
            content(str):
        """
        splitted = line.split(maxsplit=5)
        bounding = BoundingBox.from_str(' '.join(splitted[0:4]))
        return (bounding, int(splitted[4]), splitted[5])

    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)
    pagedict = defaultdict(list)
    for line in loaded:
        page = line['page']
        for item in line['content']:
            multiboxed = []
            headlinenumber = item['headlinenumber']
            headlineblocknumber = item['headlineblocknumber']
            for single_collector in item['content']:
                boxed = []
                for multibox in single_collector:
                    m_bounding = BoundingBox.from_str(multibox['bounding'])
                    m_content = multibox['content']
                    boxid, _ = [  # boxid, index
                        int(item) for item in multibox['boxed_id'].split()
                    ]
                    m_content = [_parse_box_content(item) for item in m_content]
                    boxed.append((m_bounding, (boxid, m_content)))
                multiboxed.append(boxed)
            pagedict[page].append((
                headlinenumber,
                headlineblocknumber,
                multiboxed,
            ))
    result = []
    for page, value in pagedict.items():
        result.append((page, value))
    return result
