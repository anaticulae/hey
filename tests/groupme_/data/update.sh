#! /usr/bin/bash

# footer

rawmaker -i footer/restructuredtext.pdf -o ./footer --prefix=oneline --text --char_margin=100.0

rawmaker -i footer/restructuredtext.pdf -o ./footer. --toc --text --char_margin=5.0 --border --boxes --font

# simple

rawmaker -i simple/howto_pyporting.pdf -o ./simple --toc --text --font
