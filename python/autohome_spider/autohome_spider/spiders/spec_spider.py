# #!/usr/bin/python
# # coding=utf-8
#
import scrapy
from autohome_spider.items import SpecItem
import codecs
import json
from bs4 import BeautifulSoup
import re
import sys
import os
from scrapy import log

reload(sys)
sys.setdefaultencoding('utf-8')


# 车型参配数据爬虫
class SpecSpider(scrapy.Spider):
    name = 'spec'
    allowed_domains = 'autohome.com.cn'
    start_urls = []

    def __init__(self):
        ids = self.readIds()
        self.start_urls = ['http://www.autohome.com.cn/spec/%s' % id for id in ids]

    def parse(self, response):
        url = response.url
        log.msg('[url]%s' % url)
        body = response.body
        soup = BeautifulSoup(body, 'lxml').select('.cardetail-infor')[0]
        text = str(self.gettextonly(soup)).decode('utf-8')
        m = re.findall(ur'(车身尺寸|综合油耗|厂商指导价|车身结构|整车质保|发 动 机|变 速 箱|驱动方式|二手车参考价)：\n?(.+)\n', text, re.M | re.U)
        map = dict([(d[0], d[1]) for d in m])
        result = SpecItem()
        result['id'] = url.split('/')[-1]
        result['spec'] = map
        yield result

    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    def readIds(self):

        names = filter(lambda x: 'model' in x and 'json' in x,
                       os.listdir('/Users/king/Work/code/codePool/python/autohome_spider/data'))
        print names
        if not names:
            log.msg('[spec]no model data file in data dir.', log.ERROR)
            return
        model_file_name = names[-1]
        f = codecs.open('/Users/king/Work/code/codePool/python/autohome_spider/data/%s' % model_file_name, 'r')
        ids = [line['id'] for line in json.loads(f.read())]
        log.msg(len(ids), log.INFO)
        return ids
