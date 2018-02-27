#!/usr/bin/python
# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf8')


from bs4 import BeautifulSoup
import urllib2
def fetch_weather_datas():
    # 请求页面数据
    response = urllib2.urlopen(url='http://www.weather.com.cn/weather/101010100.shtml') 
    body = response.read()

    # 用BeautifulSoup解析，取出7天的天气数据
    soup = BeautifulSoup(body, "lxml")
    tags = soup.select('#7d > ul > li')

    return ['%s\t%s\t%s\t%s' %  # 对七天的数据分别解析，将解析后的每天的数据拼接成“日期+天气+最高气温+最低气温”的字符串，\t分隔
        (
            tag.select('h1')[0].string, # 取时间数据
            tag.select('.wea')[0]['title'],  # 取天气数据
            tag.select('.tem > span')[0].string, # 取最高气温
            tag.select('.tem > i')[0].string # 取最低气温
        ) 
        for tag in tags] # 返回结果为List

# 发送邮件
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def send_mail(receivers, text):
    # 第三方 SMTP 服务
    mail_host = 'smtp.sina.com'  # 设置服务器
    mail_user = 'xxx@sina.com'  # 用户名
    mail_pass = 'xxxxxxxx'  # 口令

    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header(mail_user)
    message['To'] = Header(','.join(receivers), 'utf-8')
    message['Subject'] = Header('天气提醒', 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        log('连接服务器成功..')
        smtpObj.login(mail_user, mail_pass)
        log('登录邮箱服务器成功..')
        smtpObj.sendmail(from_addr=mail_user, to_addrs=receivers, msg=message.as_string())
        log('邮件发送成功..')
    except smtplib.SMTPException as e:
        log('无法发送邮件...' + e.message)


# 传入爬到的天气数据
def is_need_remind(weather_data):
    return '雨' in weather_data

# 从配置文件中，读取接收方邮箱地址List
def read_receivers(path):
    return [line.strip('\t') for line in open(path, 'r').readlines()]


# 日志打印
import time
def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print '[%s] %s' % (timestamp, msg)



# 主函数
def main():
    try:
        weather_datas = fetch_weather_datas()
        if is_need_remind(weather_datas[0]):
            send_mail(read_receivers('receivers.txt'), '\n'.join(weather_datas))
        else:
            log('今天天气良好')
    except Exception, e:
        log('出错..')
        send_mail(['xxxx@sina.com'], '天气提醒Job出现异常...')


# 执行主函数
main()

