#!bin/bash
. ./status.sh
function installall()
{
dir=`ls ./` #定义遍历的目录
 for i in $dir
 do
 extension="${i##*.}"
     if [ "$extension" = "gz" ] ;then
        getinstallstatus ${i%-*}
        if [ $? == 0 ] ;then
        echo "${i%-*} had installed,skip it!"
        continue
        fi
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
        getinstallstatus ${i%%[3|-]*}
        if [ $? == 0 ] ;then
        echo "${i%-*} already installed,skip it"
        continue
        fi
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
}
