# -*- coding: utf-8 -*-
BOT_NAME = 'autohome_spider'

SPIDER_MODULES = ['autohome_spider.spiders']
NEWSPIDER_MODULE = 'autohome_spider.spiders'

ROBOTSTXT_OBEY = False

# 请求时间间隔，防止被屏蔽
# DOWNLOAD_DELAY = 10

# 自动限流
AUTOTHROTTLE_ENABLED = True

# 开启的middleware
DOWNLOADER_MIDDLEWARES = {
    'autohome_spider.random_user_agent_middlewares.RandomUserAgentMiddleware': 400,
}

# 开启的pipeline
ITEM_PIPELINES = {
    'autohome_spider.pipelines.AutohomeSpiderPipeline': 300,
}

# 数据集输出路径
FEED_URI = 'data/%(name)s_%(time)s.json'
# 数据集输出格式
FEED_FORMAT = 'json'

# 日志级别
LOG_LEVEL = 'INFO'
# 日志文件路径
# LOG_FILE = 'scrapy.log'