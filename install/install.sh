#!/bin/bash 
cp libascend_ezdvpp.so /usr/lib64
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
 dir=`ls ./` #定义遍历的目录
 for i in $dir
 do
 extension="${i##*.}"
     if [ "$extension" = "gz" ] ;then
        echo "${i} is installing"
        filename=${i%.tar*}
        echo "filename:${filename}"
        if [ -d "${filename}" ];then
          rm -rf ${filename}
        fi
        tar zxvf $i > /dev/null 2>&1
        cd ${filename}
        if [ -f "setup.py" ] ;then
           python "setup.py" install > /dev/null
           cd ../
           echo "${i} installed success"
            if [ -d "${filename}" ];then
               rm -rf ${filename}
            fi
        else
           echo "${i} installed failed"
        fi
        
     elif [ "$extension" = "zip" -a "$i" != "setuptools-41.2.0.zip" ] ;then
         echo "${i} is installing"
        filename=${i%.*}
        echo "filename:${filename}"
        if [ -d "${filename}" ];then
          rm -rf ${filename}
        fi
        unzip $i > /dev/null 2>&1
        cd ${filename}
        if [ -f "setup.py" ] ;then
           python "setup.py" install
           cd ../
           echo "${i} installed success"
           if [ -d "${filename}" ];then
              rm -rf ${filename}
           fi
        else
           echo "${i} installed failed"
        fi
     fi
 done

easy_install egg/hiaiengine-py2.7.egg
bash python2_hiai_install.sh
python check.py
echo 'export LD_LIBRARY_PATH=/home/HwHiAiUser/sample-facedetection-python/facedetectionapp/hiaiapp/lib:$LD_LIBRARY_PATH' >> /etc/profile
source /etc/profile
