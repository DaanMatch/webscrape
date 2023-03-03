import scrapy
from scrapy.item import Field
from scrapy import Request
from scrapy.selector import Selector

class StateLinks(scrapy.Item):
    link = Field()

class NgosIndiaSpider(scrapy.Spider):
    name = 'ngosIndia_spider'
    allowed_domains = ['ngosindia.com']
    start_urls = ['https://ngosindia.com/ngos-of-india/']

    def parse(self, response):
        self.logger.info(f'Extract link to each state in {response}')
        
        # Print out all links to each State 
        for div in response.xpath('//*[@class="ngo-layout-cell layout-item-3"]/div[3]'):
            state = StateLinks()
            state['link'] = div.xpath('div/ul/li/strong/a//@href').extract()
            yield state

        # Get all links for each state
        for div in response.xpath('//*[@class="ngo-layout-cell layout-item-3"]/div[3]'):
            stateLinks = div.xpath('div/ul/li/strong/a//@href').getall()
            #self.logger.info(f"State Links: {stateLinks}")
            
            # Loop through all links and yield a request
            for stateLink in stateLinks:
                self.logger.info(f"State Link: {stateLink}")
                #yield Request(stateLink, self.parseState)

    def parseState(self, response):
        sel = Selector(response)
        self.logger.info(f'Extract link to each district in {sel}')
        for li in sel.xpath('//*[@class="npos-postcontent clearfix"]/ul'):
            yield {
                "districtLink": li.xpath('li/a//@href').extract()
            }
