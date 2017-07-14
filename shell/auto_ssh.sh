#!/usr/local/bin/expect -f

# 已密码的方式，自动建立ssh连接
# 使用的不是bash，而是expect,所以需要安装expect命令
# 执行方式为"expect auto_ssh.sh"

set timeout 3
set host xxx.xxx.xxx.xxx
set port 6666
set password xxxxxxxx

spawn ssh root@$ip -p $port
expect {
 "*yes/no" { send "yes\r"; exp_continue}
 "*password:" { send "$password\r" }
 }