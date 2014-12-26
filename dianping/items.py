# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianPingItem(scrapy.Item):
    stars = scrapy.Field()
    average = scrapy.Field()
    taste = scrapy.Field()
    env = scrapy.Field()
    server = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    time = scrapy.Field()
    labels = scrapy.Field()