.. _backlog:

backlog
=======

* add documentation for detector, sections, groupme at the front of `baw --doc`

* XFAIL `tests/words_/test_text.py::test_words_extract_texts_page_x[page13]`

* XFAIL `tests/words_/test_text.py::test_words_extract_texts_page_x[page14]`

* XFAIL `tests/words_/test_text.py::test_words_extract_texts_page_x[page16]`

* [ ] Improve table of content likelihood detection

* solve master_page_78_images_toc toc extraction problem /

    .. code-block:: python

        processing: toc
        could not group and parse
        [TextBoundsInfo(text='2 Geb▒audeautomation',
        bounds=TextBounds(xdist=102, ydist=302, width=136, height=12)),
        TextBoundsInfo(text='3', bounds=TextBounds(xdist=120, ydist=302,
        width=371, height=14)), TextBoundsInfo(text='2.1 Grundlagen . . . .
        . . . . . . . . . . . . . . . . . . . . . . . . 3',
        bounds=TextBounds(xdist=120, ydist=317, width=371, height=14))]
