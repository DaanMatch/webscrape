import scrapy
from scrapy.item import Field

class StateLinks(scrapy.Item):
    link = Field()

class NgosIndiaSpider(scrapy.Spider):
    name = 'ngosIndia_spider'
    allowed_domains = ['ngosindia.com']
    start_urls = ['https://ngosindia.com/ngos-of-india/']

    def parse(self, response):
        self.logger.info(f' Extract link to each state in {response}')
        
        # Print out all links to each State 
        for div in response.xpath('//*[@class="ngo-layout-cell layout-item-3"]/div[3]'):
            state = StateLinks()
            state['link'] = div.xpath('div/ul/li/strong/a//@href').extract()
            yield state
    
        stateLinks = response.xpath('//*[@class="ngo-layout-cell layout-item-3"]/div[3]')
        yield from response.follow_all(stateLinks, self.parseState)

    def parseState(self, response):
        
