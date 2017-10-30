#!/bin/bash

# 测试机总是莫名其妙地断网，找了各种法子仍然无解，只能通过工作电脑来定时ping一下了。。

ping -c2 10.252.26.228
if [ $? -ne 0 ];then
	osascript -e "display notification \"测试机断网了...\" with title \"fuck\""
fi