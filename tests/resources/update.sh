#! /usr/bin/bash

scriptpath=$(readlink -f "$0")
scriptroot=$(dirname "$scriptpath")

pushd $scriptroot

# footer

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --prefix=oneline\
         --text\
         --font\
         --char_margin=100.0\
         --boxes_flow=1.0

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --border\
         --boxes\
         --font\
         --text\
         --char_margin=5.0\
         --boxes_flow=1.0\
         --line_margin=0.3

sections -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --chapter\
         --index\
         --sections\
         --title\
         --toc\
         --whitepage
# simple

rawmaker -i simple/howto_pyporting.pdf\
         -o ./simple\
         --font\
         --text\
         --char_margin=5.0\
         --boxes_flow=1.0

popd
