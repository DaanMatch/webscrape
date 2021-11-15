import scrapy


class IndiangoSpider(scrapy.Spider):
    name = 'IndiaNGO'
    #allowed_domains = ['https://www.indiangoslist.com/ngo-address/achukuru-welfare-society-in-itanagar-arunachal-pradesh_AR-2009-0015817']
    #start_urls = ['https://www.indiangoslist.com/ngo-address/achukuru-welfare-society-in-itanagar-arunachal-pradesh_AR-2009-0015817']
    start_urls = ['https://www.indiangoslist.com/']

    def parse(self,response):
        #get all hyperlinks of states on the home page
        ngo_links = response.css("li > h3 > a::attr('href')")
        #for each links, call function parse_one
        yield from response.follow_all(ngo_links,self.parse_one) 
    def parse_one(self, response):
        #For each NGO on that page, get it into ngo_scrape
        ngo_scrape = response.css(".title > a::attr('href')")
        #call parse_two on every ngo from ngo_scrape
        yield from response.follow_all(ngo_scrape,self.parse_two)
        #gets all links from the pagination, note that scrapy automatically make sure they don't visit same links twice.
        ngo_next = response.css(".pagination > a::attr('href')")
        #call parse_one on every links because each of these links contain multiple NGO
        yield from response.follow_all(ngo_next,self.parse_one) 

    def parse_two(self, response):
        #get the left row
        ngo_left = response.css(".ngo_left_head::text").extract()
        ngo_right = response.css(".ngo_right_head::text").extract()
        #get the right row
        span = response.xpath("//*[@class='ngo_right_head']//text()").extract()
        count_1 = 0
        count_2 = 0
        #remove space and "/n"
        for i in range(len(span)):
            if span[i] == ' ':
                count_1 += 1
            elif span[i] == '\n':
                count_2 += 1
        for _ in range(count_1):
            span.remove(' ')
        for _ in range(count_2):
            span.remove('\n')
        #remove space if exist
        if ' ' in ngo_left:
            ngo_left.remove(' ')
        #make sure the left row and right row oare the same length after fixing key issues
        span = span[0:len(ngo_left)+1]
        #since the key issue has two part, we have to indentify them and add them together
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
        #export the result
        for item in zip(ngo_left,span):

            scraped = {
                'name' : item[0],
                'description' : item[1]
            }
            yield scraped
        pass