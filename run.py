__author__ = 'apple'
from scrapy import cmdline

cmdline.execute('scrapy crawl dianping1 --set LOG_FILE=log'.split())