#!/bin/bash 
. ./installall.sh

getinstallstatus setuptools
if [ $? == 1 ] ;then
echo "setuptools is installing"
if [ -d "./setuptools-41.2.0" ] ;then
rm -rf ./setuptools-41.2.0
fi
unzip ./setuptools-41.2.0.zip
cd setuptools-41.2.0
if [ ! -f "./setup.py" ] ;then
  echo setup not exit!
fi
python setup.py install > /dev/null
echo "setuptools installed success"
cd ../
if [ -d "./setuptools-41.2.0" ] ;then
rm -rf ./setuptools-41.2.0
fi
else
echo "setuptools had installed,skip it!"
 
fi
installall

getinstallstatus hiai
if [ $? == 1 ] ;then
if [ -f ""/usr/lib64/hiaiengine-py2.7.egg"" ] ;then
easy_install "/usr/lib64/hiaiengine-py2.7.egg"
bash python2_hiai_install.sh
if [ $? == "0" ] ;then
echo "hiaiengine-py install success!"
else
echo "hiaiengine-py2.7 install failed!"
exit 1
fi
else
echo "hiaiengine-py2.7.egg install failed for not exist!"
fi
else
echo "hiai had installed,skip it!" 
fi

python check.py

echo "All installation steps over!"
exit
