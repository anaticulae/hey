#! /usr/bin/bash

scriptpath=$(readlink -f "$0")
scriptroot=$(dirname "$scriptpath")

pushd $scriptroot

# footer

echo "    running rawmaker restruct oneline"

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --prefix=oneline\
         --font\
         --text\
         --toc\
         --char_margin=100.0\
         --boxes_flow=1.0

echo "    running rawmaker restruct"

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --border\
         --boxes\
         --font\
         --text\
         --toc\
         --char_margin=5.0\
         --boxes_flow=1.0\
         --line_margin=0.3

echo "    running rawmaker simple oneline"

rawmaker -i simple/howto_pyporting.pdf\
         -o ./simple\
         --prefix=oneline\
         --text\
         --font\
         --toc\
         --char_margin=100.0\
         --boxes_flow=1.0

echo "    running rawmaker simple"

rawmaker -i simple/howto_pyporting.pdf\
         -o ./simple\
         --border\
         --boxes\
         --font\
         --text\
         --toc\
         --char_margin=5.0\
         --boxes_flow=1.0\
         --line_margin=0.3

echo "    running sections restruct"

sections -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --chapter\
         --index\
         --sections\
         --title\
         --toc\
         --whitepage

echo "    running sections simple"

sections -i simple/howto_pyporting.pdf\
         -o ./simple\
         --chapter\
         --index\
         --sections\
         --title\
         --toc\
         --whitepage

popd
