#! /usr/bin/bash

scriptpath=$(readlink -f "$0")
scriptroot=$(dirname "$scriptpath")

pushd $scriptroot

ret=0

echo "    running rawmaker porting_module"

rawmaker -i porting_module/porting_module_to_python3.pdf\
         -o ./porting_module\
         --prefix=oneline\
         --font\
         --text\
         --toc\
         --char_margin=100.0\
         --boxes_flow=1.0
ret+="$?"

rawmaker -i porting_module/porting_module_to_python3.pdf\
         -o ./porting_module\
         --border\
         --boxes\
         --font\
         --text\
         --toc\
         --char_margin=5.0\
         --boxes_flow=1.0\
         --line_margin=0.3
ret+="$?"

exit $ret

# TODO: activate after problem is solved

echo "    running sections porting_module"

sections -i porting_module/porting_module_to_python3.pdf\
         -o ./porting_module\
         --chapter\
         --index\
         --sections\
         --title\
         --toc\
         --whitepage
ret+="$?"

popd

exit $ret
