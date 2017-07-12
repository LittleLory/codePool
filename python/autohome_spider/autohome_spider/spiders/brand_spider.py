#!/usr/bin/python
# coding=utf-8

import scrapy
from autohome_spider.items import BrandItem


# 品牌数据爬虫
class BrandSpider(scrapy.Spider):
    name = 'brand'
    allowed_domains = 'autohome.com.cn'
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    def parse(self, response):
        for brandPart in response.xpath('body/dl'):
            brand = BrandItem()
            brand['id'] = brandPart.xpath('@id')[0].extract()
            brand['url'] = brandPart.xpath('dt/a/@href')[0].extract()
            brand['name'] = brandPart.xpath('dt/div/a/text()')[0].extract()
            brand['pic'] = brandPart.xpath('dt/a/img/@src')[0].extract()
            yield brand
