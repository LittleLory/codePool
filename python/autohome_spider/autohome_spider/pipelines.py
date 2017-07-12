# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs


# 默认生成的pipeline，没有使用到
class AutohomeSpiderPipeline(object):
    def process_item(self, item, spider):
        return item
