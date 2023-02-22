import scrapy


class IndiangoslistSpiderSpider(scrapy.Spider):
    name = 'indiangoslist_spider'
    allowed_domains = ['indiangoslist.com']
    start_urls = ['http://indiangoslist.com/']

    def parse_home_page(self,response):
        #get all hyperlinks of states on the home page
        state_links = response.css("li > h3 > a::attr('href')")
        #for each link, call function parse_state
        yield from response.follow_all(state_links, self.parse_state)

    def parse_state(self, response):
        #For each NGO on that page, get it into ngo_links
        ngo_links = response.css(".title > a::attr('href')")
        #call parse_ngo on every ngo link
        yield from response.follow_all(ngo_links, self.parse_ngo)
        #get all links from the pagination, note that Scrapy automatically ensures that they don't visit the same links twice.
        pagination_links = response.css(".pagination > a::attr('href')")
        #call parse_state on every link because each of these links contains multiple NGOs
        yield from response.follow_all(pagination_links, self.parse_state)

    def parse_ngo(self, response):
        #get the left row and right row
        ngo_left = response.css(".ngo_left_head::text").extract()
        ngo_right = response.css(".ngo_right_head::text").extract()
        #get the right row
        span = response.xpath("//*[@class='ngo_right_head']//text()")
        
        #export the result
        for item in zip(ngo_left, span):
            scraped = {
            'name': item[0],
            'description': item[1]
            }
        yield scraped
