import scrapy
class State(scrapy.Item):
    Link = scrapy.Field()
class NgodarpanSpider(scrapy.Spider):
    # Created a spider named “ngodarpan_spider”,which sends a request to start_urls
    # and gets the response from the server
    name = 'ngodarpan_spider'
    allowed_domains = ['ngodarpan.gov.in']
    start_urls = ['https://ngodarpan.gov.in/index.php/home/statewise']

    def parse(self, response):
        if response.status == 200:
            self.logger.info("getting links to statewise lists")
            try:
                # capture all the links of states
                stateLinks = response.css("ol.rounded-list li a::attr(href)")
                # using parseState function to scrap the table correspond to each state link
                yield from response.follow_all(stateLinks, self.parseState)
            except:
                self.logger.info(f"Failed at parse for {response}.")

    def parseState(self, response):
        self.logger.info("Parse ngos in State.")
        try: 
            for row in response.xpath('//*[@class="table table-striped table-bordered table-hover Tax"]//tbody/tr'):
                yield {
                    'SrNo':  row.xpath('td[1]//text()').extract_first(),
                    'Name': row.xpath('td[2]/a//text()').extract_first(),
                    'Registration': row.xpath('td[3]//text()').extract_first(),
                    'Address': row.xpath('td[4]//text()').extract_first(),
                    'SectorWorking': row.xpath('td[5]//text()').extract_first()
                }
            # each table has many pages
            nextPage = response.css(".pagination > a::attr(href)")
            yield from response.follow_all(nextPage, self.parseState)
        except:
            self.logger.info(f"Failed at parseStates {response}.")
            pass


   


            
