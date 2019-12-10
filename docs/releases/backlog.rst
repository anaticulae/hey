.. _backlog:

backlog
=======

* add documentation for detector, sections, groupme at the front of `baw --doc`

* XFAIL `tests/words_/test_text.py::test_words_extract_texts_page_x[page13]`

* XFAIL `tests/words_/test_text.py::test_words_extract_texts_page_x[page14]`

* XFAIL `tests/words_/test_text.py::test_words_extract_texts_page_x[page16]`

* [ ] Improve table of content likelihood detection

* do not split likelihood for multi page tocs

    .. code-block:: yaml

        - content:
          - name: toc
            value: 0.26
          page: 1
        - content:
          - name: toc
            value: 0.37
          page: 2
        - content:
          - name: toc
            value: 0.22
          page: 3

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

* reduce required test power

    .. code-block:: None

        317.45s setup    test_huge.py::test_huge_sections_extractor[generated\\notitle/docu_porting_extension_modules.pdf]
        308.80s setup    test_huge.py::test_huge_running_words[generated\\notitle/docu_porting_extension_modules.pdf]
        293.01s setup    test_huge.py::test_huge_running_groupme[generated\\notitle/docu_porting_extension_modules.pdf]
        195.14s setup    test_huge.py::test_huge_running_words[generated\\notitle/bachelor_page_111_images_toc.pdf]
        183.03s setup    test_huge.py::test_huge_running_words[generated\\notitle/docu_restructuredtext.pdf]
        178.02s setup    test_huge.py::test_huge_sections_extractor[generated\\notitle/bachelor_page_111_images_toc.pdf]
        169.86s setup    test_huge.py::test_huge_sections_extractor[generated\\notitle/docu_restructuredtext.pdf]
        156.45s setup    test_huge.py::test_huge_running_groupme[generated\\notitle/bachelor_page_111_images_toc.pdf]
        154.40s setup    test_huge.py::test_huge_running_groupme[generated\\notitle/docu_restructuredtext.pdf]
        35.89s setup    test_huge.py::test_huge_running_words[docu/restructuredtext.pdf]
