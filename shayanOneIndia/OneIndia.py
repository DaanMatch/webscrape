import scrapy


class OneindiaSpider(scrapy.Spider):
    name = "OneIndia"
    allowed_domains = ["www.oneindia.com"]
    start_urls = ["http://www.oneindia.com/"]

    def parse(self, response):
        pass
