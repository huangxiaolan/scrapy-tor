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
        #"ITEM_PIPELINES":{'scrapy.pipelines.files.FilesPipeline': 1},
        #"FILES_STORE" : 'd:/tag/fordevtest'
    }
    def start_requests(self):
        urls = [
            #爬取单个页面的url
            #'http://mp.weixin.qq.com/s?src=3&timestamp=1481080517&ver=1&signature=XDh44AJ0Er8YeNxFKyl80qTwQyOxseg8ZHWb5CHojFe2czLYVFlc0BU2VtK6FU4MpgKW-o*S3afyaNqml-In8zelQbW4JxR4XhgpF5bp6nZBlC-jKI0gv0RSqQC-XT6JpGUzTlgkaPz9os*uKwQJsl-iQ5lEd79CnvpSgibPBtU='
            'https://api.github.com/'
        ]
        
        print(str(self.settings))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("success to crawl, resposne status",response.status)
        
        
    def parse_first_list(self,response):
        """
        爬取当前列表的的数据，并且如果存在下一页数据，开始爬取
        """
        #解析列表页面数据
        for listpage in self.parse_item_list(response):
            yield listpage
            
        
        self.count=self.count+1
        if self.count < self.maxPageCount :
            logging.info("-------begin to get page:%s " % self.count)
            #获取下一页的url
            #inspect_response(response, self)
            tmp_next_page=response.css("#sogou_next::attr('href')").extract_first()
            if tmp_next_page :
                next_page="http://weixin.sogou.com/weixin"+tmp_next_page
                yield scrapy.Request(url=next_page, callback=self.parse_first_list)
        
    def parse_item_list(self,response):
        """
        爬去列表数据
        """
        #inspect_response(response, self)
        items=response.css(".news-list li .txt-box h3 a::attr('href')").extract()
        #遍历返回解析详情页面数据
        for item in items:
            yield scrapy.Request(url=item, callback=self.parse_item_page)
        
        
        
        date=response.css("#post-date::text").extract_first()
        longArticle["createTime"]=date
        return longArticle
        