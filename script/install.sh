#!/usr/bin/bash
. ./status.sh

function isrootuser()
{
username=$(env | grep USER)
if [ "${USERNAME#*=}" = "root" ] ;then
return 0 
fi
return 1
}




function copyinstalldir()
{
  board_ip=$1
  echo "please input password for deploy install files"
  scp -r ../install/ HwHiAiUser@${board_ip}:/home/HwHiAiUser/ >/dev/null
  echo "deploy install files over"
}
function package_uihost()
{
getinstallstatus tornado
if [ $? == 0 ] ;then
echo "tornado had installed,skip it"
else
pip3 install tornado==5.1.0
if [ $? == "0" ] ;then
echo "tornado install success!"
else
echo "tornado install failed!"
fi
fi


getinstallstatus google.protobuf
if [ $? == 0 ] ;then
echo "protobuf had installed,skip it"
else
pip3 install protobuf==3.5.1
if [ $? == "0" ] ;then
echo "protobuf install success!"
else
echo "protobuf install failed!"
fi
fi


getinstallstatus numpy
if [ $? == 0 ] ;then
echo "numpy had installed,skip it"
else
pip3 install numpy==1.14.2
if [ $? == "0" ] ;then
echo "numpy install success!"
else
echo "numpy install failed!"
fi
fi
return 0
}

function package_host()
{
board_ip=$1
waiwang_ip=$2
usb_ip=$3
waiwang_name=$(ip addr show | grep $waiwang_ip)
if [ -z "${waiwang_name}" ] ;then
echo "outer net looks like wrong!please excute command again!"
exit
else
waiwang=${waiwang_name##* }
fi


usb_name=$(ip addr show | grep ${usb_ip})
if [ -z "$usb_name" ] ;then
echo "board net looks like wrong!please excute command again!"
exit
else
usb=${usb_name##* }
fi

echo "net1=>$waiwang"
echo "net2=>$usb"


if [ "x" == "x${waiwang}" ] ;then
echo "arg1 is null."
return 1
elif [ -z "$(ifconfig | grep -w ${waiwang})" ] ;then
echo "no interface named ${waiwang}"
return 1
fi
if [ "x" == "x${usb}" ] ;then
echo "arg2 is null."
return 1
elif [ -z "$(ifconfig | grep -w ${usb})" ] ;then
echo "no interface named ${usb}"
return 1
fi

if [ "x" == "x${board_ip}" ] ;then
board_ip="192.168.1.2"
fi
echo "1" > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o ${waiwang} -s 192.168.1.0/24 -j MASQUERADE
iptables -t nat -A POSTROUTING -o ${waiwang} -s 192.168.1.0/24 -j MASQUERADE
iptables -A FORWARD -i ${usb} -o ${waiwang} -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i ${usb} -o ${waiwang} -j ACCEPT

echo "================================================================"
echo "= Type HwHiAiUser's password on board to get board net ip name.="
echo "================================================================"

board_usb=$(ssh -t HwHiAiUser@${board_ip} "ip addr show | grep ${board_ip}")
if [ -z "${board_usb}" ] ;then
echo "board_ip looks like wrong!please excute command again!"
exit
fi
echo ${board_usb}
board_usb_name=${board_usb##* }
board_usb_name=${board_usb_name:0:${#board_usb_name}-1}
echo ${#board_usb_name}

echo "${board_usb_name}"

host_ip=$(ifconfig | grep -w -A 2 ${usb} | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | head -n1)
echo "uihost ip is ${host_ip}"
echo "======================================================="
echo "=     Type HwHiAiUser's password on board first.      ="
echo "=     Then type root's password on board.             ="
echo "======================================================="

ssh -t HwHiAiUser@${board_ip} "su - root -c \"ip route change default via ${host_ip} dev ${board_usb_name}; echo 'nameserver 114.114.114.114' > /etc/resolvconf/resolv.conf.d/base;resolvconf -u;apt-get update;apt-get upgrade;apt-get install python-dev;cd /home/HwHiAiUser/install;bash install.sh HwHiAiUser\""
return 0
}
isrootuser
if [ $? == 1 ];then
echo "please su root and then excute the shell by root user!"
exit
fi


if [ $# != 3 ] ;then
echo "input params must have three,like command bash install.sh board_ip outer_ip usb_ip"
exit
fi
copyinstalldir $@
package_uihost
package_host $@

