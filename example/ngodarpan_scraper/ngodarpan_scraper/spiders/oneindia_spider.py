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
                # Trying to click more details
                moreDetails = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "///*[@id='ngos-more-details']/a"))).click()
                ngo_count = 0
                for elem in moreDetails:
                    elem.click()
                    ngo = Ngo()
                    ngo["name"] = response.xpath('//*[@class="ngo-popup-head"]//text()').extract_first()
                    # Contact details table
                    ngo["address"] = response.xpath('//*[@class="ngo-popup-head"]//text()').extract_first()
                    ngo["city"] = scrapy.Field()
                    ngo["state"] = scrapy.Field()
                    ngo["telephone"] = scrapy.Field()
                    ngo["mobile"] = scrapy.Field()
                    ngo["website"] = scrapy.Field()
                    ngo["email"] = scrapy.Field()
                    ngo["ngoType"] = scrapy.Field()
                    ngo["regNo"] = scrapy.Field()
                    ngo["regDate"] = scrapy.Field()
                    ngo["areasOfHelp"] = scrapy.Field()
                    yield ngo
                    ngo_count += 1
            except:
                self.logger.info(f"Failed at parse for {response}.")
        else:
            self.logger.info('Invalid response.')



