#! /usr/bin/bash

scriptpath=$(readlink -f "$0")
scriptroot=$(dirname "$scriptpath")

pushd $scriptroot

# footer

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --prefix=oneline\
         --text\
         --char_margin=100.0

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --border\
         --boxes\
         --font\
         --text\
         --char_margin=5.0\
         --toc

# simple

rawmaker -i simple/howto_pyporting.pdf\
         -o ./simple\
         --font\
         --text\
         --toc

popd
