# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime

def reformat_to_df(text):
    # Initialize empty dictionaries to hold the column values
    columns = {
        'Add': [],
        'Pin': [],
        'Contact Person': [],
        'Purpose': [],
        'Aim/Objective/Mission': [],
        'Website': [],
        'Tel': [],
        'Mobile': [],
        'Email': []
    }
    # Loop through each row of the 'data' column and extract the values
    for row in text:
        # Initialize empty dictionaries to hold the values for this row
        values = {
            'Add': '',
            'Pin': '',
            'Contact Person': '',
            'Purpose': '',
            'Aim/Objective/Mission': '',
            'Website': '',
            'Tel': '',
            'Mobile': '',
            'Email': ''
        }
        # Split each element of the 'data' list on the colon (':') character
        for item in row:
            tokens = item.split(':')
            if len(tokens) == 2:
                # If the split resulted in two tokens, use them to populate the appropriate column
                key = tokens[0].strip()
                value = tokens[1].strip()
                if key in columns:
                    values[key] = value
        # Append extracted values to appropriate column lists
        for key, value in values.items():
            columns[key].append(value)

def remove_punctuation_purpose(text):
    return text.str.replace('[^\w\s,]', '')

def remove_punctuation_contact(text):
    return text.str.replace('[^\w\s\.]', '')

class NgoindiascraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
