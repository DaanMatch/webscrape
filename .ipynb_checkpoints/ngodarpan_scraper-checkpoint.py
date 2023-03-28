import scrapy


class NgodarpanScraperSpider(scrapy.Spider):
    name = 'ngodarpan_scraper'
    allowed_domains = ['ngodarpan.gov.in']
    start_urls = ['http://ngodarpan.gov.in/']

    def parse(self, response):
        pass
