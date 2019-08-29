#!bin/bash
sudo ip route change default via 192.168.1.223 dev usb0
echo nameserver 114.114.114.114 > /etc/resolvconf/resolv.conf.d/base
cat /etc/resolvconf/resolv.conf.d/base
resolvconf -u
apt-get update
apt-get upgrade
apt-get install python-dev
