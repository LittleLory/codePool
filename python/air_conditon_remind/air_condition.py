#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
北京空气质量监控，语音播报

前置条件：
1. 申请百度开发者权限，开通语音合成服务，并安装SDK。链接：http://yuyin.baidu.com/tts
2. 安装mplayer应用
3. 有扬声器

"""

import os
import urllib2
import time
import re
from aip import AipSpeech

""" 接入百度SDK"""
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
speech_client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def fetch_air_condition():
    response = urllib2.urlopen(url='http://www.86pm25.com/city/beijing.html')
    body = response.read()

    level_match = re.search(r'var qualityStr = "(.*?)"', body, re.M | re.I)
    level = '未找到数据'
    if level_match:
        level = level_match.group(1)

    pm_match = re.search(r'var idx = "(\d+?)"', body, re.M | re.I)
    pm = '未找到数据'
    if pm_match:
        pm = pm_match.group(1)

    return level, pm


def is_need_protect(pm):
    return pm >= 100


def log(msg, e=None):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print '--- ', timestamp, ' ---'
    print msg
    if e:
        print e
    print '--------\n'


def speech(words):
    voice_result = speech_client.synthesis(words, 'zh', 1, {'vol': 5, 'spd': 3})

    if not isinstance(voice_result, dict):
        filename = 'voice.mp3'
        with open(filename, 'wb+') as f:
            f.write(voice_result)

        os.system("mplayer " + filename + " > /dev/null")


def main():
    try:
        level, pm = fetch_air_condition()
        words = "空气质量播报：空气等级：" + level + ", pm2.5数值：" + pm + "。"
        if is_need_protect(pm):
            words += "今天空气较差，记得带上口罩。"

        log(words)
        for i in range(3):
            speech(words)
            time.sleep(3)
    except Exception, e:
        log('出错..', e)


if __name__ == "__main__":
    main()
