# -*- coding: utf-8 -*-

# Scrapy settings for dianping project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dianping'

SPIDER_MODULES = ['dianping.spiders']
NEWSPIDER_MODULE = 'dianping.spiders'

ITEM_PIPELINES = {
    'dianping.pipelines.DianPingPipeline': 300
}

#反ban策略一：禁用COOKIES
COOKIES_ENABLED = False

#取消默认的useragent,使用新的useragent,反ban策略二
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'dianping.spiders.rotate_useragent.RotateUserAgentMiddleware': 400
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dianping (+http://www.yourdomain.com)'
