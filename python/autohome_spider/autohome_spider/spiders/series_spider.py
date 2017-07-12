#!/usr/bin/python
# coding=utf-8

import scrapy
from autohome_spider.items import SeriesItem


# 车系数据爬虫
class SeriesSpider(scrapy.Spider):
    name = 'series'
    allowed_domains = 'autohome.com.cn'
    # start_urls = ['http://www.autohome.com.cn/grade/carhtml/A.html']
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    def parse(self, response):
        for brandPart in response.xpath('body/dl'):
            series = SeriesItem()
            brand_id = brandPart.xpath('@id')[0].extract()
            make_name = brandPart.xpath('dd/div/text()')[0].extract()
            seriesParts = brandPart.xpath('dd/ul/li')
            # print 'brandID[%s], makeName[%s], series[%s].' % (brand_id, make_name, seriesParts)
            for seriesPart in seriesParts:
                try:
                    series['brand_id'] = brand_id
                    series['make_name'] = make_name
                    series['id'] = seriesPart.xpath('@id')[0].extract()
                    series['name'] = seriesPart.xpath('h4/a/text()')[0].extract()
                    series['url'] = seriesPart.xpath('h4/a/@href')[0].re(r'(http://www\.autohome\.com\.cn/\d+)')
                    yield series
                except:
                    pass
