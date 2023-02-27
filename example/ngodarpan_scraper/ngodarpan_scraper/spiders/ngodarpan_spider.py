import scrapy
import numpy as np

class State(scrapy.Item):
    Link = scrapy.Field()

class NgoDarpanNgo(scrapy.Item): 
    SrNo = scrapy.Field()
    Name = scrapy.Field()
    Registration = scrapy.Field()
    Address = scrapy.Field()
    SectorWorking = scrapy.Field()

class NgodarpanSpider(scrapy.Spider):
    name = 'ngodarpan_spider'
    allowed_domains = ['ngodarpan.gov.in']
    start_urls = ['https://ngodarpan.gov.in/index.php/home/statewise']

    def parseStateLink(self, response):
        if response.status == 200:

            self.logger.info('Getting links to state-wise list for NGOs.')

            for stateLink in response.css('ol.rounded-list li  a::attr(href)'):
                state = State()
                state['Link'] = stateLink.extract()
                yield state
        else:
            self.logger.info('Invalid response.')

    def parse(self, response):
        if response.status == 200:
            self.logger.info("Getting links to statewise lists.")
            try:
                """
                for href in response.css("ol.rounded-list li  a::attr(href)"):
                    self.logger.info(href)
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, callback = self.parseState)
                """
                stateLinks = response.css("ol.rounded-list li  a::attr(href)")
                yield from response.follow_all(stateLinks, callback=self.parseState)
            except:
                self.logger.info(f"Failed at parse for {response}.")
        else:
            self.logger.info('Invalid response.')

    def parseState(self, response):
        self.logger.info("Parse ngos in State.")
        try: 
            yield response.css('.table>tbody>tr>td::text')[1].extract()

            for row in response.xpath('//*[@class="table table-striped table-bordered table-hover Tax"]//tbody/tr'):
                ngo = NgoDarpanNgo()
                ngo['SrNo'] = row.xpath('td[1]//text()').extract_first()
                ngo['Name'] = row.xpath('td[2]//text()').extract_first()
                ngo['Registration'] = row.xpath('td[3]//text()').extract_first()
                ngo['Address'] = row.xpath('td[4]//text()').extract_first()
                ngo['SectorWorking'] = row.xpath('td[5]//text()').extract_first()
                self.logger.info(ngo)
                yield ngo
        except:
            self.logger.info(f"Failed at parseStates {response}.")
            pass
       #nextPage = response.css(".pagination > a::attr('href')")
        #yield from response.follow_all(nextPage, self.parseState) 