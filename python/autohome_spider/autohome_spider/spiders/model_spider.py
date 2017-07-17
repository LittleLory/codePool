#!/usr/bin/python
# coding=utf-8

import json
import scrapy
from autohome_spider.items import ModelItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from autohome_spider.constants import levelMap


# 车型数据爬虫
class ModelSpider(CrawlSpider):
    name = 'model'
    allowed_domains = 'autohome.com.cn'
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    rules = (
        # 字母分区页
        Rule(SgmlLinkExtractor(allow=(r'http://www.autohome.com.cn/grade/carhtml/\S.html',)), callback='parse',
             follow=True),

        # 车系详情
        Rule(SgmlLinkExtractor(allow=(r'.*www\.autohome\.com\.cn/\d+.*',)), callback='parse_model_selling',
             follow=True),

        # 历史年款车型
        Rule(SgmlLinkExtractor(allow=(r'.*www\.autohome\.com\.cn/ashx/series_allspec\.ashx?s=\d+&y=\d+&l=\d+$',)),
             callback='parse_model_selled', follow=True),
    )

    # 解析字母分区页
    def parse(self, response):
        log.msg('[parse] %s' % response.url)

        # 解析车系ID，添加对应的车系详情页URL到request队列
        for seriesId in response.xpath('body/dl').re(r'id="s(\d+)"'):
            series_page_url = "http://www.autohome.com.cn/" + seriesId
            log.msg('series_page_url:%s' % series_page_url)
            request = scrapy.Request(url=series_page_url, callback=self.parse_model_selling, dont_filter=True)
            request.meta['series_id'] = seriesId
            yield request

    # 解析车系详情页
    def parse_model_selling(self, response):
        log.msg('[parse_selling] %s' % response.url)
        series_id = response.meta['series_id']
        log.msg('series_id: %s' % series_id)

        # 判断此车系是否是在售车系
        stop_sell = response.xpath('/html/body').re(ur'(指导价（停售）)')

        # 如果是在售车系
        if (not stop_sell) or len(stop_sell) == 0:
            log.msg('[parse_selling] is selling.')
            # 解析在售车型数据
            count = 0
            panel = response.xpath('//div[@id="speclist20"]/*')
            size = len(panel)
            if size % 2 != 0:
                log.msg('tag size[%d] is not expect, series_id[%s].' % (size, series_id), log.WARNING)
                return

            for i in range(size / 2):
                group = panel[i * 2].xpath('div/span/text()')[0].extract()

                models = panel[i * 2 + 1]
                for model in models.xpath('li'):
                    model_name = model.xpath('div[@class="interval01-list-cars"]/div/p/a/text()')[0].extract()
                    model_id = model.xpath('div[@class="interval01-list-cars"]/div/p/@data-gcjid')[0].extract()
                    price = model.xpath('div[@class="interval01-list-guidance"]/div/text()')[0].re(r'(\d+\.\d+)')
                    if not price:
                        price = model.xpath('div[@class="interval01-list-guidance"]/div/text()')[1].re(r'(\d+\.\d+)')

                    model = ModelItem()
                    model['id'] = model_id
                    model['name'] = model_name
                    model['series_id'] = series_id
                    model['group'] = group
                    model['price'] = price
                    yield model
                    count += 1

            log.msg('[parse_selling] model count is %d' % count)

            # 解析历史年款车型数据URL，并添加到request队列
            try:
                level = response.xpath("//div[@class='path fn-clear']/div/a[2]/@href")[0].extract().strip('/')
                level = levelMap[level]
            except Exception as e:
                log.msg('level not match, series_id[%s], msg[%s].' % (series_id, e.message), log.WARNING)
                return

            year_ids = response.xpath('//div[@id="drop2"]/div/ul/li/a/@data').extract()
            if not year_ids:
                log.msg('year_id not found, series_id[%s].' % series_id, log.WARNING)
                return

            for year_id in year_ids:
                url = 'http://www.autohome.com.cn/ashx/series_allspec.ashx?s=%s&y=%s&l=%s' % (series_id, year_id, level)
                request = scrapy.Request(url=url, callback=self.parse_model_selled, dont_filter=True)
                request.meta['series_id'] = series_id
                yield request

        # 如果该车系是停售车系
        else:
            log.msg('[parse_selling] is not selling.')
            count = 0
            model_tags = response.xpath('//table/tboby/tr')
            if not model_tags or len(model_tags) == 0:
                model_tags = response.xpath('//table/tr')

            for model_tag in model_tags:
                model_id = model_tag.xpath('td[@class="name_d"]/a/@href')[0].re(r'spec/(\d+)/')[0]
                model_name = model_tag.xpath('td[@class="name_d"]/a/@title')[0].extract()
                price = model_tag.xpath('td[@class="price_d"]/text()').re(ur'(\d+\.\d+)')

                model = ModelItem()
                model['id'] = model_id
                model['name'] = model_name
                model['series_id'] = series_id
                model['price'] = price
                yield model
                count += 1
            log.msg('[parse_selling] model count is %d' % count)

    # 解析历史年款车型数据
    def parse_model_selled(self, response):
        log.msg('[parse_selled] %s' % response.url)
        series_id = response.meta['series_id']
        data = json.loads(response.body_as_unicode())
        models = data['Spec']
        count = 0
        for model in models:
            model_id = model['Id']
            model_name = model['Name']
            group = model['GroupName']
            price = model['Price']

            model = ModelItem()
            model['id'] = model_id
            model['name'] = model_name
            model['series_id'] = series_id
            model['group'] = group
            model['price'] = price
            yield model
            count += 1
        log.msg('[parse_selled] model count is %d' % count)
