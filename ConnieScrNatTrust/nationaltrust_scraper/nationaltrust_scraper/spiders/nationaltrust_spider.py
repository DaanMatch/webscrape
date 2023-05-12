import scrapy
from nationaltrust_scraper.items import NGO



class NationaltrustSpider(scrapy.Spider):
    name = 'nationaltrust_spider'
    allowed_domains = ['thenationaltrust.gov.in']
    start_urls = ['https://thenationaltrust.gov.in/content/registered_organization.php']
    
    def parse(self, response):
        for row in response.xpath('//*[@class="caregiver_display"]//tbody/tr'):
            ngo = NGO()
            ngo['s_no'] = row.xpath('td[1]//text()').extract_first()
            ngo['state'] = row.xpath('td[2]//text()').extract_first()
            ngo['district'] = row.xpath('td[3]//text()').extract_first()
            ngo['organization_name'] = row.xpath('td[4]//text()').extract_first()
            ngo['email']= row.xpath('td[5]//text()').extract_first()
            ngo['address'] = row.xpath('td[6]//text()').extract_first()
            ngo['phone_no'] = row.xpath('td[7]//text()').extract_first()
            ngo['schemes_enrolled'] = row.xpath('td[8]//text()').extract_first()
            ngo['authorized_person'] = row.xpath('td[9]//text()').extract_first()
            ngo_values = list(ngo.values())
            if ngo_values[1] == None:
                continue     
            yield ngo
        
        next_url = response.xpath('/html/body/section[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[11]/td/a[contains(text(),">>")]/@href').get()
        print(next_url)
        next_page = response.urljoin(next_url)
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)
