import scrapy


class IndiangoSpider(scrapy.Spider):
    name = 'IndiaNGO'
    #allowed_domains = ['https://www.indiangoslist.com/ngo-address/achukuru-welfare-society-in-itanagar-arunachal-pradesh_AR-2009-0015817']
    #start_urls = ['https://www.indiangoslist.com/ngo-address/achukuru-welfare-society-in-itanagar-arunachal-pradesh_AR-2009-0015817']
    start_urls = ['https://www.indiangoslist.com/']

    def parse(self,response):
        ngo_links = response.css("li > h3 > a::attr('href')")
        print(ngo_links)
        yield from response.follow_all(ngo_links,self.parse_one) 
    def parse_one(self, response):
        ngo_scrape = response.css(".title > a::attr('href')")
        yield from response.follow_all(ngo_scrape,self.parse_two)
         
        ngo_next = response.css(".pagination > a::attr('href')")
        #make sure ngo_next is unique
        yield from response.follow_all(ngo_next,self.parse_one) 

    def parse_two(self, response):
        ngo_left = response.css(".ngo_left_head::text").extract()
        ngo_right = response.css(".ngo_right_head::text").extract()
        span = response.xpath("//*[@class='ngo_right_head']//text()").extract()
        count_1 = 0
        count_2 = 0
        for i in range(len(span)):
            if span[i] == ' ':
                count_1 += 1
            elif span[i] == '\n':
                count_2 += 1
        for _ in range(count_1):
            span.remove(' ')
        for _ in range(count_2):
            span.remove('\n')
        if ' ' in ngo_left:
            ngo_left.remove(' ')
        span = span[0:len(ngo_left)+1]
        if ' Key Issues ' in ngo_left:
            if ngo_left[len(ngo_left)-2] == ' Operational States ' and ngo_left[len(ngo_left)-1] == ' Operational Districts ':
                span[len(span)-4] = span[len(span)-4] + span[len(span)-3]
                span = span[0:len(span)-3] + span[len(span)-2:]
            elif ngo_left[len(ngo_left)-1] == ' Operational States ' and ngo_left[len(ngo_left)-2] == ' Operational Districts ':
                span[len(span)-4] = span[len(span)-4] + span[len(span)-3]
                span = span[0:len(span)-3] + span[len(span)-2:]
            elif ngo_left[len(ngo_left)-1] == ' Operational States ' or ngo_left[len(ngo_left)-1] == ' Operational Districts ':
                span[len(span)-3] = span[len(span)-3] + span[len(span)-2]
                span = span[0:len(span)-2] + span[len(span)-1:]
            else:
                span[len(span)-2] = span[len(span)-2] + span[len(span)-1]
                span = span[0:len(span)-1]
        for item in zip(ngo_left,span):

            scraped = {
                'name' : item[0],
                'description' : item[1]
            }
            yield scraped
        pass