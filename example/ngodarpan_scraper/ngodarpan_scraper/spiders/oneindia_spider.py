import scrapy
import numpy as np
from scrapy_selenium import SeleniumRequest



class Ngo(scrapy.Item): 
    name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    telephone = scrapy.Field()
    mobile = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    ngoType = scrapy.Field()
    regNo = scrapy.Field()
    regDate = scrapy.Field()
    areasOfHelp = scrapy.Field()


class NgodarpanSpider(scrapy.Spider):
    name = 'oneindia_spider'

    def start_requests(self):
        url = 'https://www.oneindia.com/ngos-in-chandigarh-6.html'
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response):
        if response.status == 200:
            self.logger.info(f"Running prase function on {response}")
            try:
                stateLinks = response.css("ol.rounded-list li  a::attr(href)")
                yield from response.follow_all(stateLinks, callback=self.parseState)
            except:
                self.logger.info(f"Failed at parse for {response}.")
        else:
            self.logger.info('Invalid response.')


            //*[@id="container"]/section/div/div[2]/section[2]/div/div/div[1]/div[1]