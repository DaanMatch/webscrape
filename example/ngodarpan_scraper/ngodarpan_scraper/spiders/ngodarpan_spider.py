import scrapy

class State(scrapy.Item):
    link = scrapy.Field()

class NgodarpanSpiderSpider(scrapy.Spider):
    name = 'ngodarpan_spider'
    allowed_domains = ['ngodarpan.gov.in']
    start_urls = ['https://ngodarpan.gov.in/index.php/home/statewise']

    def parse(self, response):
        if response.status == 200:

            self.logger.info('Getting links to state-wise list for NGOs.')

            for stateLink in response.css('ol.rounded-list li  a::attr(href)'):
                state = State()
                state['link'] = stateLink.extract()
                yield state
        else:
            self.logger.info('Invalid response.')
