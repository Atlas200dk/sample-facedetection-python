#!bin/bash
pip3 install tornado==5.1.0
if [ $? == "0" ] ;then
echo "tornado install success!"
else
echo "tornado already exist or install failed!"
fi
pip3 install protobuf==3.5.1
if [ $? == "0" ] ;then
echo "protobuf install success!"
else
echo "protobuf already exist or install failed!"
fi
pip3 install numpy==1.14.2
if [ $? == "0" ] ;then
echo "numpy install success!"
else
echo "numpy already exist or install failed!"
fi
sudo apt install expect
if [ $? == "0" ] ;then
echo "expect install success!"
else
echo "expect already exist or install failed!"
fi

host_ip=$(ifconfig | grep -o '192\.168\.1\.[0-9]\+' | head -n1)
if [ -z "$host_ip" ] ;then
echo ip grep error,deploy failed!
exit 1
else
echo host ip address is detected as $host_ip
fi
configFile="../facedetectionapp/graph.config"
serverConfigFile="../presenterserver/face_detection/config/config.conf"
modelFile="../facedetectionapp/graph.config.model"
serverModelFile="../presenterserver/face_detection/config/config.conf.model"
installdir="../install"
networkModelFile="../install/network.sh.model"
networkConfigFile="../install/network.sh"
if [ -f "$configFile" ]; then
  rm -f $configFile
fi

if [ -f "$serverConfigFile" ]; then
  rm -f $serverConfigFile
fi
sed "s/192.168.1.166/${host_ip}/" ${modelFile}>$configFile
sed "s/192.168.1.166/${host_ip}/" ${serverModelFile}>$serverConfigFile
sed "s/192.168.1.166/${host_ip}/" ${networkModelFile}>$networkConfigFile
echo "config has been finished"
echo "please input password for deploy code"
scp -r ../../sample-facedetection-python/ HwHiAiUser@192.168.1.2:/home/HwHiAiUser/ >/dev/null
echo "deploy over"
