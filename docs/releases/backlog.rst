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
