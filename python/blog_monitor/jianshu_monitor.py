#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
简书文章数据抓取脚本
抓取文章的阅读量、评论量、喜欢量
"""

from bs4 import BeautifulSoup
import urllib2
import re
import time
import codecs
import logging

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) != 2:
    print('usage: python jianshu_monitor.py base_path')
    exit(15)

base_path = sys.argv[1]

logger = logging.getLogger('monitor')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

file_handler = logging.FileHandler('%s/run.log' % base_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)

class RedirctHandler(urllib2.HTTPRedirectHandler):
    """docstring for RedirctHandler"""
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        result.code = 302
        return result


def http_request(url):
    opener = urllib2.build_opener(RedirctHandler)
    response = opener.open(url)
    code = response.getcode()
    body = ''
    if code == 200:
        body = response.read()
    return code, body


def parse_note_infos(body):
    soup = BeautifulSoup(body, 'lxml')
    tags = soup.select('.note-list > li')
    infos = []
    for tag in tags:
        id = tag['data-note-id']
        title = tag.select('.title')[0].text
        info = tag.select('.meta')[0].text
        match = re.match(r'\s*([-\d]+)\s*([-\d]+)\s*([-\d]+)\s*', info)

        if not match:
            logger.error('=== info ===')
            logger.error(info)
            logger.error('=== end ===')
            raise Exception('match result is None.')

        groups = match.groups()
        if len(groups) != 3:
            raise Exception('match group length[%s] is wrong.' % len(groups))

        info = {
            'id': id,
            'title': title,
            'read': groups[0],
            'comment': groups[1],
            'like': groups[2],
        }
        infos.append(info)

    infos.sort(cmp=lambda i1, i2: cmp(i1['id'], i2['id']))
    return infos


def write_info(f, info):
    timestamp = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    f.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (
        timestamp, info['id'], info['title'], info['read'], info['comment'], info['like']))
    f.flush()


def main():
    logger.info("jianshu monitor job start...")
    target_url = 'https://www.jianshu.com/u/2d48ed845229'
    try:
        i = 1
        f = codecs.open('%s/page_info.log' % base_path, 'a+')
        while True:
            url = '%s?order_by=shared_at&page=%d' % (target_url, i)
            code, body = http_request(url)
            logger.info("request: url = [%s], code = [%d]." % (url, code))
            if code == 200:
                infos = parse_note_infos(body)
                for info in infos:
                    write_info(f, info)

                i += 1
            else:
                break
    except Exception as e:
        logger.exception(e)

    logger.info("jianshu monitor job end...")


if __name__ == '__main__':
    main()

