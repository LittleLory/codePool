# -*- coding: utf-8 -*-
import scrapy


# 品牌
class BrandItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    pic = scrapy.Field()


# 车系
class SeriesItem(scrapy.Item):
    id = scrapy.Field()
    brand_id = scrapy.Field()
    make_name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


# 车型
class ModelItem(scrapy.Item):
    id = scrapy.Field()
    series_id = scrapy.Field()
    name = scrapy.Field()
    group = scrapy.Field()
