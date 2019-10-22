#!bin/bash
function copy()
{
host_ip=$(ifconfig | grep -o '192\.168\.1\.[0-9]\+' | head -n1)
if [ -z "$host_ip" ] ;then
echo ip grep error,deploy failed!
exit 1
else
echo host ip address is detected as $host_ip
fi
configFile="../../facedetectionapp/graph.config"
serverConfigFile="../../presenterserver/face_detection/config/config.conf"
modelFile="../../facedetectionapp/graph.config.model"
serverModelFile="../../presenterserver/face_detection/config/config.conf.model"
installdir="../../install"

if [ -f "$configFile" ]; then
  rm -f $configFile
fi

if [ -f "$serverConfigFile" ]; then
  rm -f $serverConfigFile
fi
sed "s/192.168.1.166/${host_ip}/" ${modelFile}>$configFile
sed "s/192.168.1.166/${host_ip}/" ${serverModelFile}>$serverConfigFile

echo "config has been finished"
echo "please input password for deploy code"
scp -r ../../../sample-facedetection-python/ $1@$2:/home/$1/ >/dev/null
echo "deploy over"
}
