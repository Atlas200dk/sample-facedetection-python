#!bin/bash
if [ $# -ne 2 ] ;then
echo "input params must have two!"
exit
fi
echo "1" > /proc/sys/net/ipv4/ip_forward
sudo iptables -t nat -A POSTROUTING -o $1 -s 192.168.1.0/24 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o $1 -s 192.168.1.0/24 -j MASQUERADE
sudo iptables -A FORWARD -i $2 -o $1 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i $2 -o $1 -j ACCEPT
echo "network config finished!"