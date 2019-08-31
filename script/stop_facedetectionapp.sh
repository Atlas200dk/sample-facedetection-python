#!/usr/bin/expect

set username [lrange $argv 0 0]
set passwd [lrange $argv 1 1]

if { "$username" == "" } {
        puts "Default Username is:HwHiAiUser@192.168.1.2"
        set username HwHiAiUser@192.168.1.2
} 
if { "$passwd" == "" } {
        puts "Default Password is:Mind@123"
        set passwd Mind@123
} 



spawn ssh $username@$ip
expect {
	"(yes/no)?" {  send "yes\r";exp_continue }
	"password:" { send "$passwd\r" }
}

expect "$username"
send "su root\r"
expect "Password"
send "${passwd}\r"
expect "root"
send "cd sample-facedetection-python\r"
expect "root"
send "python stop.py\r"
expect eof
interact
