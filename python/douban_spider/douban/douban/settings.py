# -*- coding: utf-8 -*-

# Scrapy settings for douban project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

ROBOTSTXT_OBEY = False

# 开启的middleware
DOWNLOADER_MIDDLEWARES = {
    'douban.random_user_agent_middlewares.RandomUserAgentMiddleware': 400,
}

# 自动限流
AUTOTHROTTLE_ENABLED = True

# 数据集输出路径
FEED_URI = '%(name)s_%(time)s.csv'
# 数据集输出格式
FEED_FORMAT = 'csv'

# 日志级别
LOG_LEVEL = 'INFO'
# 日志文件路径
# LOG_FILE = 'scrapy.log'