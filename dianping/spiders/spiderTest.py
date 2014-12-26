#!/usr/bin/python
# -*- coding:utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
import scrapy

from dianping.items import DianPingItem


class DianPingSpider(Spider):
    """爬取大众点评一个页面信息"""
    #log.start("log",loglevel='INFO')
    name = "dianping1"
    allowed_domains = ["www.dianping.com"]

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0'
        return [scrapy.Request("http://www.dianping.com/shop/19363280",
                headers={'User-Agent': user_agent})]

    def parse(self, response):

        sel = Selector(response)
        sites = sel.xpath('//div[@id="basic-info"]/div[1]/span')
        raw_phone = sel.xpath('//div[@id="basic-info"]/p[1]/span[2]')
        raw_address = sel.xpath('//div[@id="basic-info"]/div[2]/span[2]')
        raw_time = sel.xpath('//div[@id="basic-info"]/div[3]/p[2]/span[2]')
        #批量获取标签
        words = sel.xpath('//div[@id="basic-info"]/div[3]/p[5]/span[position()>1]')
        item = DianPingItem()
        keywords = ''
        length = len(words)
        count = 0

        stars = sites[0].xpath('@title').extract()
        average = sites[2].xpath('text()').extract()
        taste = sites[3].xpath('text()').extract()
        env = sites[4].xpath('text()').extract()
        server = sites[5].xpath('text()').extract()
        phone = raw_phone.xpath('text()').extract()
        address = raw_address.xpath('text()').extract()
        time = raw_time.xpath('text()').extract()

        for site in words:
            word = site.xpath('a/text()').extract()
            number = site.xpath('text()').extract()
            keyword = word[0].encode('utf-8') + number[1].strip().encode('utf-8')
            count += 1
            if count < length:
                keywords = keywords + keyword + ',' + ' '
            else:
                keywords = keywords + keyword

        item['stars'] = [s.encode('utf-8') for s in stars]
        item['average'] = [a.encode('utf-8') for a in average]
        item['taste'] = [t.encode('utf-8') for t in taste]
        item['env'] = [e.encode('utf-8') for e in env]
        item['server'] = [s1.encode('utf-8') for s1 in server]
        item['phone'] = [p.encode('utf-8') for p in phone]
        item['address'] = [address[0].strip()]
        item['time'] = [time[0].strip()]
        item['labels'] = [keywords]

        log.msg("Append done.", level='INFO')
        return item
