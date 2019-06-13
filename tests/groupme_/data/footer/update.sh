#! /usr/bin/bash

rawmaker -i restructuredtext.pdf -o . --prefix=oneline --text --char_margin=100.0

rawmaker -i restructuredtext.pdf -o . --toc --text --char_margin=5.0 --border --boxes --font
