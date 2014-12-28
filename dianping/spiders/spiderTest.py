#!/usr/bin/python
# -*- coding:utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
import scrapy

from dianping.items import DianPingItem

scrapy.Request
class DianPingSpider(Spider):
    """爬取大众点评一个页面信息"""
    #log.start("log",loglevel='INFO')
    name = "dianping1"
    allowed_domains = ["www.dianping.com"]
    download_delay = 2
    start_urls = ["http://www.dianping.com/shop/18525714",
                  "http://www.dianping.com/shop/21029470",
                  "http://www.dianping.com/shop/18016330",
                  "http://www.dianping.com/shop/19363280"]
    '''def start_requests(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0'
        return [scrapy.Request("http://www.dianping.com/shop/19363280",
                headers={'User-Agent': user_agent})]'''

    def parse(self, response):

        sel = Selector(response)
        sites = sel.xpath('//div[@id="basic-info"]/div[1]/span')
        raw_phone = sel.xpath('//div[@id="basic-info"]/p[1]/span[2]')
        raw_address = sel.xpath('//div[@id="basic-info"]/div[2]/span[2]')

        #不同页面的time位置不同，顾做一个判断
        raw_time = sel.xpath('//div[@id="basic-info"]/div[3]/p[2]/span[2]')
        words = sel.xpath('//div[@id="basic-info"]/div[3]/p[5]/span[position()>1]')
        if raw_time == []:
            raw_time = sel.xpath('//div[@id="basic-info"]/div[3]/p[1]/span[2]')
            words = sel.xpath('//div[@id="basic-info"]/div[3]/p[4]/span[position()>1]')

        #批量获取标签
        item = DianPingItem()
        keywords = ''
        length = len(words)
        count = 0

        stars = sites[0].xpath('@title').extract()

        '''average = sites[2].xpath('text()').extract()
        taste = sites[3].xpath('text()').extract()
        env = sites[4].xpath('text()').extract()
        server = sites[5].xpath('text()').extract()'''
        #跳过第一个星级，因为星级抓取的时title，自行处理
        flag = True
        counts = ''
        for member in sites:
            if flag == True:
                flag = False
            else:
                tmp = member.xpath('text()').extract()[0]
                counts = counts + tmp + ', '

        phone = raw_phone.xpath('text()').extract()
        address = raw_address.xpath('text()').extract()
        times = raw_time.xpath('text()').extract()[0].strip().split('\n')
        final_time = ''
        time_flag = True
        for time in times:
            if time_flag == True:
                final_time = final_time + time
                time_flag = False
            else:
                final_time = final_time + ', ' + time

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
        '''item['average'] = [a.encode('utf-8') for a in average]
        item['taste'] = [t.encode('utf-8') for t in taste]
        item['env'] = [e.encode('utf-8') for e in env]
        item['server'] = [s1.encode('utf-8') for s1 in server]'''
        item['counts'] = [counts.encode('utf-8')]
        item['phone'] = [p.encode('utf-8') for p in phone]
        item['address'] = [address[0].strip()]
        item['time'] = [final_time.encode('utf-8')]
        item['labels'] = [keywords]

        log.msg("Append done.", level='INFO')
        return item
