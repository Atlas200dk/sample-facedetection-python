#!/usr/bin/expect
set username HwHiAiUser
set ip 192.168.1.2
set passwd Mind@123

spawn ssh $username@$ip
expect {
	"(yes/no)?" {  send "yes\r";exp_continue }
	"password:" { send "$passwd\r" }
}

#expect "$username"
#send "su root\r"
#expect "Password"
#send "${passwd}\r"
expect "$username"
send "cd sample-facedetection-python/facedetectionapp\r"
expect "$username"
send "python main.py\r"
expect eof
interact
