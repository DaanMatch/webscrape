import scrapy
import numpy as np

class NgodarpanSpider(scrapy.Spider):
    name = 'oneindia_spider'
    allowed_domains = ['oneindia.com']
    start_urls = ['https://www.oneindia.com/ngos-in-chandigarh-6.html']

    def parse(self, response):
        if response.status == 200:
            self.logger.info("Getting links to statewise lists.")
            try:
                stateLinks = response.css("ol.rounded-list li  a::attr(href)")
                yield from response.follow_all(stateLinks, callback=self.parseState)
            except:
                self.logger.info(f"Failed at parse for {response}.")
        else:
            self.logger.info('Invalid response.')