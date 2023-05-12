# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

def remove_newlines(s):
    return s.replace('\n', '')

def remove_rchar(s):
    return s.replace('\r', '')

def remove_tchar(s):
    return s.replace('\t', '')

def capitalize_names(s):
    names = s.split()
    cp_names = [name.title() for name in names]
    return " ".join(cp_names)

def format_phoneno(s):
	return s[:4] + "-" + s[4:]

def clean_schema(s):
    actual_schemas = ['Niramaya', 'Disha', 'Vikaas', 'Samarth', 
    'Gharaunda', 'Prerna', 'Sahyogi', 'Sambhav', 'Gyan Prabha', 'Badhte Kadam']
    schemas = s.split()
    for i in range(len(schemas) - 1):
        if schemas[i] in actual_schemas and schemas[i+1] in actual_schemas:
            schemas[i] += ','
    return ''.join(schemas)

# Define the custom ItemLoader for the NGO class
class NGOItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    s_no_in = MapCompose(str.strip)
    state_in = MapCompose(str.strip, capitalize_names)
    district_in = MapCompose(remove_newlines, remove_rchar, remove_tchar, str.strip, capitalize_names)
    organization_name_in = MapCompose(str.strip, capitalize_names)
    email_in = MapCompose(str.strip)
    address_in = MapCompose(str.strip, remove_newlines, remove_rchar, remove_tchar, capitalize_names)
    phone_no_in = MapCompose(str.strip, format_phoneno)
    schemes_enrolled_in = MapCompose(remove_newlines, remove_rchar, remove_tchar, str.strip, clean_schema)
    authorized_person_in = MapCompose(str.strip, capitalize_names)
       

class NGO(scrapy.Item):
    """
    A class to represent an NGO and its information.

    Attributes:
        s_no (scrapy.Field): The entry number of the NGO.
        state (scrapy.Field): The state where the NGO is located.
        district (scrapy.Field): The district where the NGO is located.
        organization_name (scrapy.Field): The name of the NGO.
        email (scrapy.Field): The email address of the NGO.
        address (scrapy.Field): The physical address of the NGO.
        phone_no (scrapy.Field): The phone number of the NGO.
        schemes_enrolled (scrapy.Field): The schemes, or area of help served by the NGO.
        authorized_person (scrapy.Field): The authorized person of the NGO.
    """
    s_no = scrapy.Field(
        serializable_name='S.No.'
        )
    state = scrapy.Field(
        input_processor=NGOItemLoader.state_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='State'
        )
    district = scrapy.Field(
        input_processor=NGOItemLoader.district_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='District'
        )
    organization_name = scrapy.Field(
        input_processor=NGOItemLoader.organization_name_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='Organization Name'
        )
    email = scrapy.Field(
        input_processor=NGOItemLoader.email_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='Email'
        )
    address = scrapy.Field(
        input_processor=NGOItemLoader.address_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='Address'
        )
    phone_no = scrapy.Field(
        input_processor=NGOItemLoader.phone_no_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='Phone No.'
        )
    schemes_enrolled = scrapy.Field(
        input_processor=NGOItemLoader.schemes_enrolled_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='Schemes Enrolled'
        )
    authorized_person = scrapy.Field(
        input_processor=NGOItemLoader.authorized_person_in,
        output_processor=NGOItemLoader.default_output_processor,
        serializable_name='Authorized Person'
        )
