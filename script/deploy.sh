#!/usr/bin/bash
. ./deploy/copy.sh
. ./deploy/network.sh


if [ $# != 4 ] ;then
echo "input params must have four,like command username ip ensxx ensxx"
exit
fi
cd deploy
copy $@
network $@


