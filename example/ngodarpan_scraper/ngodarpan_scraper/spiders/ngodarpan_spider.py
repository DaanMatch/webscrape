import scrapy


class NgodarpanSpiderSpider(scrapy.Spider):
    name = 'ngodarpan_spider'
    allowed_domains = ['ngodarpan.gov.in']
    start_urls = ['https://ngodarpan.gov.in/index.php/home/statewise']

    def parse(self, response):
        self.logger.info('Getting links to state-wise list for NGOs.')
        stateLinks = response.css(".bluelink11px > a::attr('href')")
        for stateLink in stateLinks:
            yield stateLinks.get()
        
