#!/bin/bash

function network()
{
interface_1=$3
interface_2=$4
board_ip=$2
if [ "x" == "x${interface_1}" ] ;then
echo "arg1 is null."
return 1
elif [ -z "$(ifconfig | grep -w ${interface_1})" ] ;then
echo "no interface named ${interface_1}"
return 1
fi
if [ "x" == "x${interface_2}" ] ;then
echo "arg2 is null."
return 1
elif [ -z "$(ifconfig | grep -w ${interface_2})" ] ;then
echo "no interface named ${interface_2}"
return 1
fi

if [ "x" == "x${board_ip}" ] ;then
board_ip="192.168.1.2"
fi

echo "${interface_1}"
echo "${interface_2}"
echo "1" > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o ${interface_1} -s 192.168.1.0/24 -j MASQUERADE
iptables -t nat -A POSTROUTING -o ${interface_1} -s 192.168.1.0/24 -j MASQUERADE
iptables -A FORWARD -i ${interface_2} -o ${interface_1} -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i ${interface_2} -o ${interface_1} -j ACCEPT

host_ip=$(ifconfig | grep -w -A 2 ${interface_2} | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | head -n1)
echo "======================================================="
echo "=     Type HwHiAiUser's password on board first.      ="
echo "=     Then type root's password on board.             ="
echo "======================================================="
ssh -t HwHiAiUser@${board_ip} "su - root -c \"ip route change default via ${host_ip} dev usb0; echo 'nameserver 114.114.114.114' > /etc/resolvconf/resolv.conf.d/base;resolvconf -u;apt-get update;apt-get upgrade;apt-get install python-dev\""
return 0

}

