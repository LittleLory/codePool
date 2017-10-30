# #!/usr/bin/python
# # coding=utf-8
#
import scrapy
import codecs
import json
from bs4 import BeautifulSoup
import re
import sys
import os
import chardet
from autohome_spider.items import DetailItem
from scrapy import log

reload(sys)
sys.setdefaultencoding('utf-8')


# 车型参配数据爬虫
class Detail(scrapy.Spider):
    name = 'detail'
    allowed_domains = 'autohome.com.cn'
    start_urls = []

    def __init__(self):
        ids = self.readIds()
        self.start_urls = ['http://car.autohome.com.cn/config/spec/%s.html' % id for id in ids]

    def parse(self, response):
        url = response.url
        log.msg('[url]%s' % url)

        current = int(url.split('/')[-1].split('.')[0])

        body = response.body


        matcher = re.search(r'var specIDs =\[(.*)\];', body)
        if not matcher:
            log.msg('modelId[%s], no data...' % current)
            return
        data = matcher.group(1)
        model_ids = data.split(',')
        if str(current) not in model_ids:
            log.msg('modelId[%s], no current data...' % current)
            return

        detail = {}

        # print '==============================='

        matcher = re.search(r'var config = (\{.*\});', body)
        data = matcher.group(1)
        encoding = chardet.detect(data)['encoding']
        j = json.loads(data, encoding=encoding)

        for config_types in j['result']['paramtypeitems']:
            for config_items in config_types['paramitems']:
                id = config_items['id']
                # name = config_items['name']
                # detail_name = DetailItem()
                # detail_name['id'] = id
                # detail_name['name'] = name
                # yield detail_name
                # print '------ id[%s] ------' % id
                values = config_items['valueitems']
                for value in values:
                    if current == value['specid']:
                        detail[id] = value['value']

        # print '==============================='

        matcher = re.search(r'var option = (\{.*\});', body)
        data = matcher.group(1)
        encoding = chardet.detect(data)['encoding']
        j = json.loads(data, encoding=encoding)

        for config_types in j['result']['configtypeitems']:
            for config_items in config_types['configitems']:
                id = config_items['id']
                # name = config_items['name']
                # detail_name = DetailItem()
                # detail_name['id'] = id
                # detail_name['name'] = name
                # yield detail_name
                # print '------ id[%s] ------' % id
                values = config_items['valueitems']
                for value in values:
                    if current == value['specid']:
                        detail[id] = value['value']

        detail_item = DetailItem()
        detail_item['id'] = current
        detail_item['detail'] = detail
        yield detail_item

    def readIds(self):

        names = filter(lambda x: 'model' in x and 'json' in x,
                       os.listdir('/home/king/code/python_job/autohome_spider/data'))
        print names
        if not names:
            log.msg('[spec]no model data file in data dir.', log.ERROR)
            return
        model_file_name = names[-1]
        f = codecs.open('/home/king/code/python_job/autohome_spider/data/%s' % model_file_name, 'r')
        ids = [line['id'] for line in json.loads(f.read())]
        log.msg(len(ids), log.INFO)
        return ids
