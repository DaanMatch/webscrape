import scrapy
from scrapy.item import Field
'''
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy_selenium import SeleniumRequest
'''



class oneIndiaAttribute(scrapy.Item):
    name = Field()
    address = Field()
    sectorWorkingIn = Field()
    '''
    city = Field()
    state = Field()
    telephone = Field()
    mobile = Field()
    website = Field()
    email = Field()
    ngoType = Field()
    registrationNo = Field()
    dateOfRegistration = Field()
    areasOfHelp = Field()
    '''

class oneIndiaSpider(scrapy.Spider):
    name = "oneIndia"
    allowed_domains = ["www.oneindia.com"]
    start_urls = ["https://www.oneindia.com/ngos.html"]

    def parse(self, response):
        stateLinks = response.css('div.ngo-state-btn-list ul li a::attr(href)')
        yield from response.follow_all(stateLinks, self.parseState)
        """
        for ngo in response.css('div.reg-detail-table'):
        oneIndiaNgo = oneIndiaAttribute()
        oneIndiaNgo['address'] = ngo.css('table.table1 tbody td').get()
        ##//*[@id="data-container"]/div[1]/div[3]/a
        """   

    def parseState(self, response):
        for ngo in response.css('div.ngo-found-block'):

            oneIndiaNgo = oneIndiaAttribute()
            oneIndiaNgo['name'] = ngo.css('div.foundation-title::text').get()
            oneIndiaNgo['address'] = ngo.css('div.address-dtl::text').get()
            oneIndiaNgo['sectorWorkingIn'] = ngo.css('div.sector-details::text').get()
            yield oneIndiaNgo
            ##put in sectors working in later

