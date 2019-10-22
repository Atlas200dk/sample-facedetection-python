#!/usr/bin/bash

function copy()
{
if [ $# != 2 ] ;then
echo deploy error!command should be like bash deploy.sh 192.168.1.2 192.168.1.223
exit
fi
board_ip=$1
host_ip=$2
echo host_ip is $host_ip
configFile="../facedetectionapp/graph.config"
serverConfigFile="../presenterserver/face_detection/config/config.conf"
modelFile="../facedetectionapp/graph.config.model"
serverModelFile="../presenterserver/face_detection/config/config.conf.model"

if [ -f "$configFile" ]; then
  rm -f $configFile
fi

if [ -f "$serverConfigFile" ]; then
  rm -f $serverConfigFile
fi
sed "s/192.168.1.166/${host_ip}/" ${modelFile}>$configFile
sed "s/192.168.1.166/${host_ip}/" ${serverModelFile}>$serverConfigFile

echo "config has been finished"
echo "please input board login password for deploy code"
maindir=`cd ../; pwd`
scp -r ${maindir} HwHiAiUser@${board_ip}:/home/HwHiAiUser/sample-facedetection-python >/dev/null
echo "deploy over"
exit
}

copy $@
