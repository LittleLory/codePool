#!/usr/bin/python
# coding=utf-8
import scrapy
import sys

from scrapy import log

reload(sys)
sys.setdefaultencoding('utf-8')

from douban.items import BookName


class BookNameSpider(scrapy.Spider):
    name = "book_name"
    allowed_domains = 'douban.com'
    start_urls = []

    def __init__(self):
        ids = {}
        f = open('data/douban.dat', 'r')
        for line in f.readlines():
            book_id = line.split('\t')[1]
            if book_id not in ids:
                ids.setdefault(book_id)

        for id in ids.keys():
            self.start_urls.append('https://book.douban.com/subject/%s' % id)
        # print 'url size:', len(self.start_urls)

    def parse(self, response):
        book_id = response.url.strip('/').split('/')[-1]
        log.msg('book_id[%s].' % book_id)
        book_name = response.xpath('//title/text()')[0].extract().strip(' (豆瓣)')
        bean = BookName()
        bean['book_id'] = book_id
        bean['book_name'] = book_name
        yield bean
