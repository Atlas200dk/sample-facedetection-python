#!/usr/bin/bash

function setpackage()
{

ip route change default via $1 dev $2
echo 'nameserver 114.114.114.114' > /etc/resolvconf/resolv.conf.d/base
resolvconf -u
apt-get update
apt-get upgrade
apt-get install python-dev
cd /home/HwHiAiUser/install
bash install.sh HwHiAiUser
}

setpackage $@
