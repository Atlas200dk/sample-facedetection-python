#!/usr/bin/bash
username=$1
if [ "$#"="0" ];then
echo default login username is HwHiAiUser@192.168.1.2
username="HwHiAiUser@192.168.1.2"
fi
echo -----------------------------------------
echo -"input the login board password"       -
echo -----------------------------------------

ssh -t ${username} "cd /home/HwHiAiUser/sample-facedetection-python/facedetectionapp; python stop.py"

