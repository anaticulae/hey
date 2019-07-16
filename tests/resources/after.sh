#! /usr/bin/bash

scriptpath=$(readlink -f "$0")
scriptroot=$(dirname "$scriptpath")

pushd $scriptroot


echo "    running words restruct"

words -i restruct\
       --headlines\
      --boxed\
      --list\
      --text\
      --words\
      -o ./restruct

echo "    running words simple"

#words -i simple\
#       --headlines\
#      --boxed\
#      --list\
#      --text\
#      --words\
#      -o ./simple


popd
