import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Request

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


class OneIndiaSpider(scrapy.Spider):
    name = 'oneindia_spider'
    allowed_domains = ["oneindia.com"]

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.oneindia.com/ngos-in-chandigarh-6.html#',
            callback=self.parse
        )

    def parse2(self, response):
        self.logger.info(f'Extract link to each state in {response}')
        #get all hyperlinks of states on the home page
        stateLinks = self.driver.find_elements_by_css_selector('.ngo-state-btn-block div ul li a::attr("href")')
        #for each links, call function parseState
        for link in stateLinks:
            url = link.get_attribute("href")
            yield Request(url, callback=self.parseState)    
        # Note the website splits the NGOs by state and also by NGO sectors, so there may be duplicates. These can be processed later.

    def parse(self, response):
        self.logger.info(f'Extract information to each ngo in {response}')
        # Scroll to the bottom of the page to load all elements
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for i in response.css('div.ngo-found-block'):
            ngo = Ngo()
            ngo['name'] = i.css('div.foundation-title::text').get()
            yield ngo
        """
        # wait for the more details button to be present
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ngos-more-details']/a//@href")))
        moreDetailsButtons = self.driver.find_elements_by_xpath("//*[@id='ngos-more-details']/a//@href")
        ngo_count = 0
        # Loop through all more details buttons
        for i in range(len(moreDetailsButtons)):
            # Click the ith button to open ith overlay
            moreDetailsButtons[i].click()
            self.logger.info(f'Button {i} clicked')
            # Scrape overlay data
            ngo = Ngo()
            ngo["name"] = response.xpath('//*[@class="ngo-popup-head"]//text()').get()
            # Contact details table
            ngo["address"] = response.xpath('//*[@class="ngo-popup-container"]/div[2]/div[2]/table/tbody/tr[1]/td[2]//text()').get()
            ngo["city"] = response.xpath('//*[@class="ngo-popup-container"]/div[2]/div[2]/table/tbody/tr[2]/td[2]//text()').get()
            ngo["state"] = response.xpath('//*[@class="ngo-popup-container"]/div[2]/div[2]/table/tbody/tr[3]/td[2]//text()').get()
            ngo["telephone"] = response.xpath('//*[@class="ngo-popup-container"]/div[2]/div[2]/table/tbody/tr[4]/td[2]//text()').get()
            ngo["mobile"] = response.xpath('//*[@class="ngo-popup-container"]/div[2]/div[2]/table/tbody/tr[5]/td[2]//text()').get()
            ngo["website"] =response.xpath('//*[@class="ngo-popup-container"]/div[2]/div[2]/table/tbody/tr[6]/td[2]//text()').get()
            ngo["email"] = response.xpath('//*[@class="ngo-popup-container"]/div[2]/div[2]/table/tbody/tr[7]/td[2]//text()').get()
            # Registration details table
            ngo["ngoType"] = response.xpath('//*[@class="ngo-popup-container"]/div[3]/div[2]/table/tbody/tr[1]/td[2]//text()').get()
            ngo["regNo"] = response.xpath('//*[@class="ngo-popup-container"]/div[3]/div[2]/table/tbody/tr[2]/td[2]//text()').get()
            ngo["regDate"] = response.xpath('//*[@class="ngo-popup-container"]/div[3]/div[2]/table/tbody/tr[3]/td[2]//text()').get()
            # Areas of help table
            ngo["areasOfHelp"] = response.xpath('//*[@class="ngo-popup-container"]/div[4]/div[2]/table/tbody/tr[1]/td//text()').get()
            yield ngo 
            ngo_count += 1
        """

    
    def closed(self, reason):
        self.driver.quit()

