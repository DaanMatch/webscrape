# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime

def remove_newlines(s):
    return s.replace('\n|\r|\t', '')

def replace_newlines(s):
    return s.replace('\n|\r|\t', ' ')

class NgodarpanScraperItem(scrapy.Item):
    # define all the fields for your item here like:
    # name = scrapy.Field()

    SrNo = scrapy.Field()

    Name = scrapy.Field(
        input_processor=MapCompose(str.strip, replace_newlines, str.title),
        output_processor=TakeFirst()
    )

    Registration = scrapy.Field(
        input_processor=MapCompose(str.strip, replace_newlines, str.title),
        output_processor=TakeFirst()
    )

    Address = scrapy.Field(
        input_processor=MapCompose(str.strip, replace_newlines, str.title),
        output_processor=TakeFirst()
    )

    SectorWorking = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    
    