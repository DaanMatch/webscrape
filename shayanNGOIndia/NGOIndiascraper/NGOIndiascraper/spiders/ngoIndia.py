import scrapy
from scrapy.item import Field

class NgosIndiaSpider(scrapy.Spider):
    name = 'ngosIndia_spider'
    allowed_domains = ['ngosindia.org']
    start_urls = ['https://ngosindia.org/ngos-india/']

    def parse(self, response):
        self.logger.info(f'Extract link to each state in {response}')
        #get all hyperlinks of states on the home page
        stateLinks = response.css('.npos-layout-cell ul li a::attr("href")')
        #for each links, call function parseState
        yield from response.follow_all(stateLinks, self.parseState)      

    def parseState(self, response):
        self.logger.info(f'Extract link to each ngo in {response}')
        #get all hyperlinks of ngos on the state page
        ngoLinks = response.css('.lcp_catlist li a::attr("href")')
        #for each links, call function parseNGo
        yield from response.follow_all(ngoLinks, self.parseNGO)
        #gets all links from the pagination

        ngo_next = response.css(".lcp_paginator li a::attr('href')")
        #call parseState on every links 
        yield from response.follow_all(ngo_next,self.parseState) 
        

    def parseNGO(self, response):
        self.logger.info(f'Extract ngo information in {response}')
        #get all hyperlinks of ngos on the state page
        yield {
            ##run another script for website urls 
            ##'website' : response
            'name' : response.css('h1.npos-postheader ::text').getall()
            ##'data': response.css('.npos-postcontent p ::text').getall()
        }