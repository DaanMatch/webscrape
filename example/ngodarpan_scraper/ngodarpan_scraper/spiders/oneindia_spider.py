import scrapy
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    allowed_domains = ["oneindia.com"]

    def start_requests(self):
        url = 'https://www.oneindia.com/ngos-in-chandigarh-6.html'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # driver = webdriver.Chrome()  # To open a new browser window and navigate it
        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        if response.status == 200:
            self.logger.info(f"Running parse function on {response}")
            try:
                stateLinks = response.css("ol.rounded-list li  a::attr(href)")
                yield from response.follow_all(stateLinks, callback=self.parseState)
            except:
                self.logger.info(f"Failed at parse for {response}.")
        else:
            self.logger.info('Invalid response.')

//*[@id="container"]/section/div/div[2]/section[2]/div/div/div[1]/div[1]
            //*[@id="container"]/section/div/div[2]/section[2]/div/div/div[1]/div[1]