# -*- coding=utf8 -*-
import scrapy
from scrapy.shell import inspect_response
import logging

class WxSpider(scrapy.Spider):
    count=0
    maxPageCount=100 #爬取最多页数
    name = "wx"
    custom_settings={
        "User-Agent":"User-Agent,Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "ROBOTSTXT_OBEY": False,
        #"ITEM_PIPELINES":{'weixin_spider.pipelines.StoreMongoLongArticlePipeline': 1},
        "CONCURRENT_REQUESTS":2, #一次最多发送两个web请求。
        
    }
    def start_requests(self):
        urls = [
            #爬取单个页面的url
            
            'https://api.github.com/'
        ]
        
        print(str(self.settings))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("success to crawl, resposne status",response.status)
        
        

        