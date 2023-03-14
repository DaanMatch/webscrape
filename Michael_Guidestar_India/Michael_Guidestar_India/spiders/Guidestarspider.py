import scrapy


class GuidestarspiderSpider(scrapy.Spider):
    name = "Guidestarspider"
    allowed_domains = ["guidestarindia.org"]
    start_urls = ["https://guidestarindia.org/NGOs4IndiaGenerosityRun.aspx"]

    def parse(self, response):
        self.logger.info(f"Browse ngos in {response}.")
       
        ngo_count = 0
        for row in response.xpath('//*[@id="SectionPlaceHolder2"]/table/tbody/tr'):
            yield {
                'SrNo':  row.xpath('td[1]//text()').extract_first(),
                'NGO Name': row.xpath('td[2]//text()').extract_first(),
                'Donation Coupon Code': row.xpath('td[3]//text()').extract_first(),
                'NGO works for': row.xpath('td[4]//text()').extract_first(),
                'NGO can provide 80G Receipt on request': row.xpath('td[5]//text()').extract_first(),
                'Foreign nationals can run for this NGO': row.xpath('td[6]//text()').extract_first(),
                'GuideStar India Certification Level': row.xpath('td[7]//text()').extract_first(),
                'To know more about the NGO, view its Transaprency Profile on GuideStar India ': row.xpath('td[8]//text()').extract_first(),

            }
            ngo_count += 1


        self.logger.info(f"Total number of NGos in {response}: {ngo_count}")


