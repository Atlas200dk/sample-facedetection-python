#!/bin/bash 
. ./installall.sh
cp libascend_ezdvpp.so /usr/lib64
if [ $? == "0" ] ;then
echo "libascend_ezdvpp.so copy success!"
else
echo "libascend_ezdvpp.so copy failed!"
exit 1
fi
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
 
installall


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


python check.py
if [ -z "$LD_LIBRARY_PATH" ] ;then
echo 'export LD_LIBRARY_PATH=/home/HwHiAiUser/sample-facedetection-python/facedetectionapp/hiaiapp/lib:$LD_LIBRARY_PATH' >> /etc/profile
source /etc/profile
echo "environment config success!"
else
echo "environment already exist!"
fi
